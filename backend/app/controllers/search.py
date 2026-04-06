from typing import TYPE_CHECKING

from db import provide_transaction
from db.schema import ORMCorpus, ORMDocument
from db.util import escape_search_query
from litestar import Controller, get
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
from openai import AsyncOpenAI  # noqa: TC002
from paradedb.sqlalchemy import pdb, search
from sqlalchemy import (
    and_,
    desc,
    func,
    select,
    tuple_,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

# TODO: remove pyright ignores once sqlalchemy-paradedb matures


class SearchController(Controller):
    """Controller that handles search-related API endpoints."""

    dependencies = {
        "db_transaction": Provide(provide_transaction),
        "openai_client": Provide(provide_client),
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
        where_clause = [search.parse(ORMDocument.text, escape_search_query(q))]  # pyright: ignore[reportArgumentType]
        if corpus_name is not None:
            corpus_pkeys_sq = select(ORMCorpus.pkey).where(
                ORMCorpus.name.in_(corpus_name)
            )
            where_clause.append(ORMDocument.corpus_pkey.in_(corpus_pkeys_sq))

        # count the total number of hits
        sql_count = select(func.count(ORMDocument.pkey)).where(and_(*where_clause))

        # results for the current page only
        sql_results_sq = (
            select(  # pyright: ignore[reportCallIssue]
                ORMDocument.id,
                ORMDocument.corpus_pkey,
                pdb.score(ORMDocument.pkey).label("score"),  # pyright: ignore[reportArgumentType,reportAttributeAccessIssue]
                pdb.snippet(
                    ORMDocument.text,  # pyright: ignore[reportArgumentType]
                    start_tag="<b>",
                    end_tag="</b>",
                    max_num_chars=500,
                ),
            )
            .where(and_(*where_clause))
            .order_by(desc("score"))
            .order_by(ORMDocument.pkey)
            .offset(offset)
            .limit(num_results)
        ).subquery()

        # use a subquery to get the corpus names only for the current results
        sql_results = (
            select(sql_results_sq, ORMCorpus.name)
            .join(ORMCorpus)
            .order_by(desc("score"))
        )

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

    @get(path="/get_answer", cache=True, media_type="text/event-stream")
    async def get_answer(
        self,
        db_transaction: "AsyncSession",
        openai_client: AsyncOpenAI | None,
        model_name: str,
        q: str,
        corpus_name: list[str],
        document_id: list[str],
    ) -> Stream:
        """Generate an answer using RAG.

        :param db_transaction: A DB transaction.
        :param openai_client: An OpenAI client.
        :param model_name: The model to use.
        :param q: The search query/question.
        :param corpus_name: Corpus identifiers for the corresponding documents.
        :param num_documents: IDs of documents to use for RAG.
        :raises HTTPException: When the OpenAI API is not available.
        :raises HTTPException: When the document identifiers are not properly provided.
        :raises HTTPException: When the answer could not be generated.
        :return: The answer stream.
        """
        if openai_client is None:
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
            stream = await openai_client.completions.create(
                model=model_name,
                prompt=get_rag_prompt(q, doc_inputs),
                stream=True,
            )
            return Stream(chunk.choices[0].text async for chunk in stream)
        except Exception as e:
            raise HTTPException(
                "Failed to generate answer.",
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                extra={"error": str(e)},
            )
