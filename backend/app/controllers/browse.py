from typing import TYPE_CHECKING, Literal

from db import provide_transaction
from db.schema import (
    ORMCorpus,
    ORMDataset,
    ORMDocument,
    ORMQRel,
    ORMQuery,
)
from litestar import Controller, get
from litestar.di import Provide
from litestar.exceptions import HTTPException
from litestar.response import Stream
from litestar.status_codes import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from llm import ensure_model_available, provide_client
from llm.util import get_summary_prompt
from models import (
    Corpus,
    Dataset,
    Document,
    DocumentInfo,
    Paginated,
    QRel,
    Query,
    QueryInfo,
)

# litestar needs the type outside of the type checking block
from openai import AsyncOpenAI  # noqa: TC002
from paradedb.sqlalchemy import pdb, search
from sqlalchemy import (
    and_,
    asc,
    desc,
    func,
    select,
    text,
)
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

# TODO: remove pyright ignores once sqlalchemy-paradedb matures


class BrowseController(Controller):
    """Controller that handles browse-related API endpoints."""

    dependencies = {
        "db_transaction": Provide(provide_transaction),
        "openai_client": Provide(provide_client),
    }

    @get(path="/get_corpora", cache=True)
    async def get_corpora(self, db_transaction: "AsyncSession") -> list[Corpus]:
        """List all corpora including statistics about datasets and documents.

        Results are ordered by corpus name.

        :param db_transaction: A DB transaction.
        :return: The list of corpora.
        """
        sq_documents = (
            select(ORMDocument.corpus_pkey, func.count().label("count"))
            .group_by(ORMDocument.corpus_pkey)
            .subquery()
        )
        sq_datasets = (
            select(ORMDataset.corpus_pkey, func.count().label("count"))
            .group_by(ORMDataset.corpus_pkey)
            .subquery()
        )

        sql = (
            select(
                ORMCorpus,
                func.coalesce(sq_documents.c.count, 0),
                func.coalesce(sq_datasets.c.count, 0),
            )
            .outerjoin(sq_documents)
            .outerjoin(sq_datasets)
            .order_by(ORMCorpus.name.asc())
        )

        result = (await db_transaction.execute(sql)).all()
        return [
            Corpus(
                name=corpus.name,
                language=corpus.language,
                num_datasets=num_datasets,
                num_documents=num_documents,
            )
            for corpus, num_documents, num_datasets in result
        ]

    @get(path="/get_datasets", cache=True)
    async def get_datasets(
        self, db_transaction: "AsyncSession", corpus_name: str
    ) -> list[Dataset]:
        """List all datasets for a corpus, including statistics.

        Results are ordered by dataset name.

        :param db_transaction: A DB transaction.
        :param corpus_name: The name of the corpus.
        :return: The list of datasets.
        """
        sq_queries = (
            select(ORMQuery.dataset_pkey, func.count().label("count"))
            .group_by(ORMQuery.dataset_pkey)
            .subquery()
        )

        sql = (
            select(ORMDataset, func.coalesce(sq_queries.c.count, 0))
            .outerjoin(sq_queries)
            .join(ORMCorpus)
            .where(ORMCorpus.name == corpus_name)
            .order_by(ORMDataset.name.asc())
        )

        result = (await db_transaction.execute(sql)).all()
        return [
            Dataset(
                name=dataset.name,
                corpus_name=corpus_name,
                relevance_threshold=dataset.relevance_threshold,
                num_queries=num_queries,
            )
            for dataset, num_queries in result
        ]

    @get(path="/get_queries", cache=True)
    async def get_queries(
        self,
        db_transaction: "AsyncSession",
        corpus_name: str,
        dataset_name: str,
        match: str | None = None,
        num_results: int = 10,
        offset: int = 0,
        order_by: Literal["relevant_documents", "length", "match_score"] | None = None,
        order_by_desc: bool = True,
    ) -> Paginated[Query]:
        """List queries.

        :param db_transaction: A DB transaction.
        :param corpus_name: The name of the corpus.
        :param dataset_name: Return only queries in this dataset.
        :param match: Return only queries matching this.
        :param num_results: How many queries to return.
        :param offset: Offset for pagination.
        :param order_by: In what order to return the queries.
        :param order_by_desc: Whether to order in a descending or ascending fashion.
        :return: Paginated list of queries.
        """
        if order_by == "match_score" and match is None:
            raise HTTPException(
                "Cannot order queries by match score without a match query.",
                status_code=HTTP_400_BAD_REQUEST,
                extra={"order_by": order_by, "match": match},
            )

        where_clause = [ORMCorpus.name == corpus_name, ORMDataset.name == dataset_name]
        if match is not None:
            where_clause.append(
                search.match_any(
                    ORMQuery.text,  # pyright: ignore[reportArgumentType]
                    match,
                )
            )

        sql_count = (
            select(func.count())
            .select_from(ORMQuery)
            .join(ORMDataset)
            .join(ORMCorpus)
            .where(*where_clause)
        )

        order_by_op = desc if order_by_desc else asc
        if order_by == "relevant_documents":
            order_by_clause = (order_by_op(text("count")), ORMQuery.pkey)
        elif order_by == "length":
            order_by_clause = (
                order_by_op(func.length(ORMQuery.text)),
                ORMQuery.pkey,
            )
        else:
            order_by_clause = (ORMQuery.pkey,)

        select_from = ORMQuery
        group_by_clause = [
            ORMQuery.pkey,
            ORMQuery.id,
            ORMQuery.description,
            ORMQuery.text,
            ORMDataset.name,
        ]

        # compute score before qrel joins/grouping so paradedb keeps the search context
        if order_by == "match_score":
            sq_query_scores = (
                select(
                    ORMQuery.pkey,
                    pdb.score(ORMQuery.pkey).label("score"),  # pyright: ignore[reportAttributeAccessIssue, reportArgumentType]
                )
                .select_from(ORMQuery)
                .join(ORMDataset, onclause=ORMQuery.dataset_pkey == ORMDataset.pkey)
                .join(ORMCorpus, onclause=ORMDataset.corpus_pkey == ORMCorpus.pkey)
                .where(*where_clause)
                .subquery()
            )
            select_from = sq_query_scores.join(
                ORMQuery, onclause=ORMQuery.pkey == sq_query_scores.c.pkey
            )
            group_by_clause.append(sq_query_scores.c.score)
            order_by_clause = (order_by_op(sq_query_scores.c.score), ORMQuery.pkey)

        sql = (
            select(
                ORMQuery.id,
                ORMQuery.text,
                ORMQuery.description,
                func.count()
                .filter(ORMQRel.relevance >= ORMDataset.relevance_threshold)
                .label("count"),
                ORMDataset.name,
            )
            .select_from(select_from)
            .join(ORMDataset, onclause=ORMQuery.dataset_pkey == ORMDataset.pkey)
            .outerjoin(ORMQRel)
            .join(ORMCorpus, onclause=ORMDataset.corpus_pkey == ORMCorpus.pkey)
            .where(*where_clause)
            .group_by(*group_by_clause)
            .order_by(*order_by_clause)
            .limit(num_results)
            .offset(offset)
        )

        total_num_results = (await db_transaction.execute(sql_count)).scalar_one()
        result = (await db_transaction.execute(sql)).all()
        return Paginated[Query](
            items=[
                Query(
                    id=id,
                    corpus_name=corpus_name,
                    dataset_name=dataset_name,
                    text=text,
                    description=description,
                    num_relevant_documents=num_rel_docs,
                )
                for id, text, description, num_rel_docs, dataset_name in result
            ],
            offset=offset,
            total_num_items=total_num_results,
        )

    @get(path="/get_query", cache=True)
    async def get_query(
        self,
        db_transaction: "AsyncSession",
        corpus_name: str,
        dataset_name: str,
        query_id: str,
    ) -> Query:
        """Return a single specific query.

        :param db_transaction: A DB transaction.
        :param corpus_name: The name of the corpus.
        :param dataset_name: The dataset name.
        :param query_id: The query ID.
        :raises HTTPException: When the query does not exist.
        :return: The query object.
        """
        sql = (
            select(
                ORMQuery,
                func.count(ORMQRel.document_pkey).filter(
                    ORMQRel.relevance >= ORMDataset.relevance_threshold
                ),
            )
            .join(ORMDataset)
            .join(ORMCorpus)
            .outerjoin(ORMQRel)
            .where(
                and_(
                    ORMQuery.id == query_id,
                    ORMCorpus.name == corpus_name,
                    ORMDataset.name == dataset_name,
                )
            )
            .group_by(ORMQuery.pkey)
        )

        try:
            db_query, num_rel_docs = (await db_transaction.execute(sql)).one()
        except NoResultFound:
            raise HTTPException(
                "Could not find the requested query.",
                status_code=HTTP_404_NOT_FOUND,
                extra={
                    "query_id": query_id,
                    "dataset_name": dataset_name,
                    "corpus_name": corpus_name,
                },
            )
        return Query(
            id=db_query.id,
            corpus_name=corpus_name,
            dataset_name=dataset_name,
            text=db_query.text,
            description=db_query.description,
            num_relevant_documents=num_rel_docs,
        )

    @get(path="/get_document", cache=True)
    async def get_document(
        self, db_transaction: "AsyncSession", corpus_name: str, document_id: str
    ) -> Document:
        """Return a single specific document.

        :param db_transaction: A DB transaction.
        :param corpus_name: The corpus name.
        :param document_id: The document ID.
        :raises HTTPException: When the document does not exist.
        :return: The document object.
        """
        sql = (
            select(
                ORMDocument,
                func.count(ORMQRel.query_pkey).filter(
                    ORMQRel.relevance >= ORMDataset.relevance_threshold
                ),
            )
            .join(ORMCorpus)
            .outerjoin(ORMQRel)
            .outerjoin(ORMQuery)
            .outerjoin(ORMDataset)
            .where(ORMCorpus.name == corpus_name, ORMDocument.id == document_id)
        ).group_by(ORMDocument.pkey)

        try:
            db_document, num_rel_queries = (await db_transaction.execute(sql)).one()
        except NoResultFound as e:
            raise HTTPException(
                "Could not find the requested document.",
                status_code=HTTP_404_NOT_FOUND,
                extra={
                    "document_id": document_id,
                    "corpus_name": corpus_name,
                    "error_code": e.code,
                },
            )
        return Document(
            id=db_document.id,
            title=db_document.title,
            text=db_document.text,
            corpus_name=corpus_name,
            num_relevant_queries=num_rel_queries,
        )

    @get(path="/get_documents", cache=True)
    async def get_documents(
        self,
        db_transaction: "AsyncSession",
        corpus_name: str,
        match: str | None = None,
        num_results: int = 10,
        offset: int = 0,
        order_by: Literal["relevant_queries", "length", "match_score"] | None = None,
        order_by_desc: bool = True,
    ) -> Paginated[Document]:
        """List documents.

        :param db_transaction: A DB transaction.
        :param corpus_name: The name of the corpus.
        :param match: Return only documents matching this.
        :param num_results: How many documents to return.
        :param offset: Offset for pagination.
        :param order_by: In what order to return the documents.
        :param order_by_desc: Whether to order in a descending or ascending fashion.
        :return: Paginated list of documents.
        """
        if order_by == "match_score" and match is None:
            raise HTTPException(
                "Cannot order documents by match score without a match query.",
                status_code=HTTP_400_BAD_REQUEST,
                extra={"order_by": order_by, "match": match},
            )

        where_clause = [ORMCorpus.name == corpus_name]
        if match is not None:
            where_clause.append(
                search.match_any(
                    ORMDocument.text,  # pyright: ignore[reportArgumentType]
                    match,
                )
            )

        sql_count = (
            select(func.count())
            .select_from(ORMDocument)
            .join(ORMCorpus, onclause=ORMDocument.corpus_pkey == ORMCorpus.pkey)
            .where(*where_clause)
        )

        document_pkey = ORMDocument.pkey
        score = None
        select_from = ORMDocument
        sq_where_clause = where_clause

        # compute score before qrel joins/grouping so paradedb keeps the search context
        if order_by == "match_score":
            sq_document_scores = (
                select(
                    ORMDocument.pkey,
                    pdb.score(ORMDocument.pkey).label("score"),  # pyright: ignore[reportAttributeAccessIssue, reportArgumentType]
                )
                .select_from(ORMDocument)
                .join(ORMCorpus, onclause=ORMDocument.corpus_pkey == ORMCorpus.pkey)
                .where(*where_clause)
                .subquery()
            )
            document_pkey = sq_document_scores.c.pkey
            score = sq_document_scores.c.score
            select_from = sq_document_scores.join(
                ORMDocument, onclause=ORMDocument.pkey == document_pkey
            )
            sq_where_clause = []

        select_clause_sq = [
            document_pkey,
            func.count()
            .filter(ORMQRel.relevance >= ORMDataset.relevance_threshold)
            .label("count"),
        ]
        group_by_clause = [document_pkey]

        order_by_op = desc if order_by_desc else asc
        if order_by == "relevant_queries":
            order_by_clause = [order_by_op(text("count"))]
        elif order_by == "length":
            select_clause_sq.append(ORMDocument.text_length.label("text_length"))
            order_by_clause = [order_by_op(text("text_length"))]
        elif score is not None:
            select_clause_sq.append(score)
            group_by_clause.append(score)
            order_by_clause = [order_by_op(text("score"))]
        else:
            order_by_clause = []

        # select pkeys of matching documents in correct order
        sq_document_pkeys = (
            select(*select_clause_sq)
            .select_from(select_from)
            .join(ORMCorpus, onclause=ORMDocument.corpus_pkey == ORMCorpus.pkey)
            .outerjoin(ORMQRel)
            .outerjoin(ORMQuery)
            .outerjoin(ORMDataset)
            .where(*sq_where_clause)
            .group_by(*group_by_clause)
            .order_by(*order_by_clause, document_pkey)
            .limit(num_results)
            .offset(offset)
        ).subquery()

        select_clause = [
            ORMDocument.id,
            ORMDocument.title,
            ORMDocument.text,
            sq_document_pkeys.c.count,
        ]

        if "text_length" in sq_document_pkeys.c:
            select_clause.append(sq_document_pkeys.c.text_length)
        if "score" in sq_document_pkeys.c:
            select_clause.append(sq_document_pkeys.c.score)
        sql = (
            select(*select_clause)
            .select_from(sq_document_pkeys)
            .join(ORMDocument, onclause=sq_document_pkeys.c.pkey == ORMDocument.pkey)
            .order_by(*order_by_clause, ORMDocument.pkey)
        )

        total_num_results = (await db_transaction.execute(sql_count)).scalar_one()
        result = (await db_transaction.execute(sql)).all()
        return Paginated[Document](
            items=[
                Document(
                    id=id,
                    corpus_name=corpus_name,
                    title=title,
                    text=text,
                    num_relevant_queries=num_rel_queries,
                )
                for id, title, text, num_rel_queries, *_ in result
            ],
            offset=offset,
            total_num_items=total_num_results,
        )

    @get(path="/get_qrels", cache=True)
    async def get_qrels(
        self,
        db_transaction: "AsyncSession",
        corpus_name: str,
        document_id: str | None = None,
        dataset_name: str | None = None,
        query_id: str | None = None,
        match_query: str | None = None,
        match_document: str | None = None,
        num_results: int = 10,
        offset: int = 0,
        order_by: Literal[
            "relevance",
            "query_length",
            "document_length",
            "query_match_score",
            "document_match_score",
        ]
        | None = None,
        order_by_desc: bool = True,
    ) -> Paginated[QRel]:
        """Return query-document pairs annotated as relevant.

        :param db_transaction: A DB transaction.
        :param corpus_name: The corpus name.
        :param document_id: Return QRels for this document only.
        :param dataset_name: Return QRels for this dataset only.
        :param query_id: Return QRels for this query only.
        :param match_query: Return only queries matching this.
        :param match_document: Return only documents matching this.
        :param num_results: How many QRels to return.
        :param offset: Offset for pagination.
        :param order_by: In what order to return the QRels.
        :param order_by_desc: Whether to order in a descending or ascending fashion.
        :return: Paginated list of QRels, ordered by relevance.
        """
        score_order_matches: dict[str | None, tuple[str | None, str, str]] = {
            "query_match_score": (
                match_query,
                "match_query",
                "Cannot order QRels by query match score without a query match.",
            ),
            "document_match_score": (
                match_document,
                "match_document",
                "Cannot order QRels by document match score without a document match.",
            ),
        }
        score_order_match = score_order_matches.get(order_by)
        if score_order_match is not None and score_order_match[0] is None:
            _, match_param, message = score_order_match
            raise HTTPException(
                message,
                status_code=HTTP_400_BAD_REQUEST,
                extra={"order_by": order_by, match_param: None},
            )

        where_clause = [
            ORMCorpus.name == corpus_name,
            ORMQRel.relevance >= ORMDataset.relevance_threshold,
        ]
        if document_id is not None:
            where_clause.append(ORMDocument.id == document_id)
        if dataset_name is not None:
            where_clause.append(ORMDataset.name == dataset_name)
        if query_id is not None:
            where_clause.append(ORMQuery.id == query_id)
        if match_query is not None:
            where_clause.append(
                search.match_any(
                    ORMQuery.text,  # pyright: ignore[reportArgumentType]
                    match_query,
                )
            )
        if match_document is not None:
            where_clause.append(
                search.match_any(
                    ORMDocument.text,  # pyright: ignore[reportArgumentType]
                    match_document,
                )
            )

        sql_count = (
            select(func.count())
            .select_from(ORMQRel)
            .join(ORMQuery)
            .join(ORMDocument)
            .join(ORMDataset)
            .join(ORMCorpus)
            .where(and_(*where_clause))
        )

        order_by_op = desc if order_by_desc else asc
        if order_by == "relevance":
            order_by_clause = (
                order_by_op(ORMQRel.relevance),
                ORMQRel.query_pkey,
                ORMQRel.document_pkey,
            )
        elif order_by == "query_length":
            order_by_clause = (
                order_by_op(func.length(ORMQuery.text)),
                ORMQRel.query_pkey,
                ORMQRel.document_pkey,
            )
        elif order_by == "document_length":
            order_by_clause = (
                order_by_op(func.length(ORMDocument.text)),
                ORMQRel.query_pkey,
                ORMQRel.document_pkey,
            )
        elif order_by == "query_match_score":
            order_by_clause = (
                order_by_op(pdb.score(ORMQuery.pkey)),  # pyright: ignore[reportArgumentType]
                ORMQRel.query_pkey,
                ORMQRel.document_pkey,
            )
        elif order_by == "document_match_score":
            order_by_clause = (
                order_by_op(pdb.score(ORMDocument.pkey)),  # pyright: ignore[reportArgumentType]
                ORMQRel.query_pkey,
                ORMQRel.document_pkey,
            )
        else:
            order_by_clause = (ORMQRel.query_pkey, ORMQRel.document_pkey)

        sql = (
            select(ORMQRel)
            .join(ORMQuery)
            .join(ORMDocument)
            .join(ORMDataset)
            .join(ORMCorpus)
            .options(
                joinedload(ORMQRel.document).joinedload(ORMDocument.corpus),
                joinedload(ORMQRel.query)
                .joinedload(ORMQuery.dataset)
                .joinedload(ORMDataset.corpus),
            )
            .where(and_(*where_clause))
            .order_by(*order_by_clause)
            .offset(offset)
            .limit(num_results)
        )

        total_num_results = (await db_transaction.execute(sql_count)).scalar_one()
        result = (await db_transaction.execute(sql)).scalars()
        return Paginated[QRel](
            items=[
                QRel(
                    query_info=QueryInfo(
                        id=qrel.query.id,
                        text=qrel.query.text,
                        description=qrel.query.description,
                    ),
                    document_info=DocumentInfo(
                        id=qrel.document.id,
                        title=qrel.document.title,
                        text=qrel.document.text,
                    ),
                    relevance=qrel.relevance,
                    corpus_name=qrel.document.corpus.name,
                    dataset_name=qrel.query.dataset.name,
                )
                for qrel in result
            ],
            offset=offset,
            total_num_items=total_num_results,
        )

    @get(path="/get_document_summary", cache=True, media_type="text/event-stream")
    async def get_document_summary(
        self,
        db_transaction: "AsyncSession",
        openai_client: AsyncOpenAI | None,
        corpus_name: str,
        document_id: str,
        model_name: str,
    ) -> Stream:
        """Stream a generated summary of a single document.

        :param db_transaction: A DB transaction.
        :param openai_client: An OpenAI client.
        :param corpus_name: The corpus name.
        :param document_id: The document ID.
        :param model_name: The model to use.
        :raises HTTPException: When the OpenAI API or requested model is not available.
        :raises HTTPException: When the document does not exist.
        :raises HTTPException: When the document could not be summarized.
        :return: The document summary stream.
        """
        sql = (
            select(ORMDocument)
            .join(ORMCorpus)
            .where(ORMCorpus.name == corpus_name, ORMDocument.id == document_id)
        )

        try:
            db_document = (await db_transaction.execute(sql)).scalar_one()
        except NoResultFound as e:
            raise HTTPException(
                "Could not find the requested document.",
                status_code=HTTP_404_NOT_FOUND,
                extra={
                    "document_id": document_id,
                    "corpus_name": corpus_name,
                    "error_code": e.code,
                },
            )

        openai_client = await ensure_model_available(openai_client, model_name)
        try:
            stream = await openai_client.completions.create(
                model=model_name,
                prompt=get_summary_prompt(db_document.text, db_document.title),
                stream=True,
            )
            return Stream(chunk.choices[0].text async for chunk in stream)
        except Exception as e:
            raise HTTPException(
                "Failed to summarize document.",
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                extra={"error": str(e)},
            )
