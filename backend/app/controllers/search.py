from typing import TYPE_CHECKING

from db import provide_transaction
from db.schema import ORMCorpus, ORMDocument
from db.util import escape_search_query
from litestar import Controller, MediaType, get
from litestar.di import Provide
from litestar.exceptions import HTTPException
from litestar.response import Stream
from litestar.status_codes import (
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_503_SERVICE_UNAVAILABLE,
)
from llm import provide_client
from llm.util import get_rag_prompt
from models import (
    DocumentSearchHit,
    Paginated,
)

# litestar needs the type outside of the type checking block
from ollama import AsyncClient  # noqa: TC002
from sqlalchemy import (
    VARCHAR,
    Integer,
    SQLColumnExpression,
    and_,
    desc,
    func,
    literal_column,
    select,
    tuple_,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class SearchController(Controller):
    """Controller that handles search-related API endpoints."""

    dependencies = {
        "db_transaction": Provide(provide_transaction),
        "ollama_client": Provide(provide_client),
    }

    @get(path="/search_documents", cache=True)
    async def search_documents(
        self,
        db_transaction: "AsyncSession",
        q: str,
        corpus_name: list[str] | None = None,
        num_results: int = 10,
        offset: int = 0,
    ) -> Paginated[DocumentSearchHit]:
        """Search documents (using full-text search).

        :param db_transaction: A DB transaction.
        :param q: The search query.
        :param corpus_name: Search only within these corpora.
        :param num_results: How many hits to return.
        :param offset: Offset for pagination.
        :return: Paginated list of results, ordered by score.
        """
        where_clause: list[SQLColumnExpression] = [
            ORMDocument.text.bool_op("@@@")(escape_search_query(q))
        ]
        if corpus_name is not None:
            corpus_cte = (
                select(ORMCorpus.pkey).where(ORMCorpus.name.in_(corpus_name)).cte()
            )

            # use ParadeDB's set filter: https://docs.paradedb.com/documentation/full-text/filtering#set-filter
            corpus_pkey_agg = select(
                func.concat(
                    "IN [",
                    func.string_agg(
                        func.cast(corpus_cte.c.pkey, VARCHAR), literal_column("' '")
                    ),
                    "]",
                )
            )
            where_clause.append(
                ORMDocument.corpus_pkey.bool_op("@@@")(
                    corpus_pkey_agg.scalar_subquery()
                )
            )

        # count the total number of hits
        sql_count = select(func.count(ORMDocument.pkey)).where(and_(*where_clause))

        # results for the current page only
        sql_results_sq = (
            select(
                ORMDocument.id,
                ORMDocument.corpus_pkey,
                func.paradedb.score(ORMDocument.pkey).label("score"),
                func.paradedb.snippet(
                    ORMDocument.text,
                    literal_column("'<b>'"),
                    literal_column("'</b>'"),
                    literal_column("500", Integer),
                ),
            )
            .where(and_(*where_clause))
            .order_by(desc("score"))
            .order_by(ORMDocument.id)
            .offset(offset)
            .limit(num_results)
        ).subquery()

        # use a subquery to get the corpus names only for the current results
        sql_results = select(sql_results_sq, ORMCorpus.name).join(ORMCorpus)

        total_num_results = (await db_transaction.execute(sql_count)).scalar_one()
        results = (await db_transaction.execute(sql_results)).all()
        return Paginated[DocumentSearchHit](
            items=[
                DocumentSearchHit(
                    id=id,
                    corpus_name=corpus_name,
                    snippet=snippet,
                    score=score,
                )
                for id, _, score, snippet, corpus_name in results
            ],
            offset=offset,
            total_num_items=total_num_results,
        )

    @get(path="/get_answer", cache=True, media_type=MediaType.TEXT)
    async def get_answer(
        self,
        db_transaction: "AsyncSession",
        ollama_client: AsyncClient | None,
        model_name: str,
        q: str,
        corpus_name: list[str],
        document_id: list[str],
    ) -> Stream:
        """Generate an answer using RAG.

        :param db_transaction: A DB transaction.
        :param ollama_client: An Ollama client.
        :param model_name: The model to use.
        :param q: The search query.
        :param corpus_name: Corpus identifiers for the corresponding documents.
        :param num_documents: IDs of documents to use for RAG.
        :raises HTTPException: When Ollama is not available.
        :raises HTTPException: When the document identifiers are not properly provided.
        :raises HTTPException: When the requested model is not available.
        :raises HTTPException: When the answer could not be generated.
        :return: The answer stream.
        """
        if ollama_client is None:
            raise HTTPException(
                "LLM services not available.",
                status_code=HTTP_503_SERVICE_UNAVAILABLE,
            )

        if len(corpus_name) != len(document_id) or len(document_id) == 0:
            raise HTTPException(
                "Must provide at least one matching corpus-document pair.",
                status_code=HTTP_400_BAD_REQUEST,
                extra={"corpus_name": corpus_name, "document_id": document_id},
            )

        try:
            await ollama_client.show(model_name)
        except Exception:
            raise HTTPException(
                "Requested model is not available.",
                status_code=HTTP_400_BAD_REQUEST,
                extra={"model_name": model_name},
            )

        sql = (
            select(ORMDocument.title, ORMDocument.text)
            .join(ORMCorpus)
            .where(
                tuple_(ORMCorpus.name, ORMDocument.id).in_(
                    list(zip(corpus_name, document_id))
                )
            )
        )
        documents = (await db_transaction.execute(sql)).all()
        doc_inputs = [(title, text) for title, text in documents]
        try:
            stream = await ollama_client.generate(
                model=model_name,
                prompt=get_rag_prompt(q, doc_inputs),
                stream=True,
                think=False,
            )
            return Stream(chunk["response"] async for chunk in stream)
        except Exception as e:
            raise HTTPException(
                "Failed to summarize document.",
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                extra={"error": str(e)},
            )
