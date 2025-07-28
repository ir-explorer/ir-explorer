from typing import TYPE_CHECKING, Literal

from db import provide_transaction
from db.schema import ORMCorpus, ORMDataset, ORMDocument, ORMQRel, ORMQuery
from db.util import escape_search_query
from litestar import Controller, get
from litestar.di import Provide
from litestar.exceptions import HTTPException
from litestar.status_codes import (
    HTTP_404_NOT_FOUND,
)
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


class BrowseController(Controller):
    """Controller that handles browse-related API endpoints."""

    dependencies = {"transaction": Provide(provide_transaction)}

    @get(path="/get_corpora", cache=True)
    async def get_corpora(self, transaction: "AsyncSession") -> list[Corpus]:
        """List all corpora including statistics about datasets and documents.

        :param transaction: A DB transaction.
        :return: The list of corpora.
        """
        sq_documents = (
            select(ORMDocument.corpus_pkey, func.count().label("count"))
            .group_by(ORMDocument.corpus_pkey)
            # this where clause is a hack to have ParadeDB perform the count aggregation
            # rather than postgres
            # TODO: remove once no longer necessary
            .where(ORMDocument.corpus_pkey.bool_op("@@@")(">0"))
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
        )

        result = (await transaction.execute(sql)).all()
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
        self, transaction: "AsyncSession", corpus_name: str
    ) -> list[Dataset]:
        """List all datasets for a corpus, including statistics.

        :param transaction: A DB transaction.
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
        )

        result = (await transaction.execute(sql)).all()
        return [
            Dataset(
                name=dataset.name,
                corpus_name=corpus_name,
                min_relevance=dataset.min_relevance,
                num_queries=num_queries,
            )
            for dataset, num_queries in result
        ]

    @get(path="/get_queries", cache=True)
    async def get_queries(
        self,
        transaction: "AsyncSession",
        corpus_name: str,
        dataset_name: str,
        match: str | None = None,
        num_results: int = 10,
        offset: int = 0,
        order_by: Literal["relevant_documents", "length", "match_score"] | None = None,
        order_by_desc: bool = True,
    ) -> Paginated[Query]:
        """List queries.

        :param transaction: A DB transaction.
        :param corpus_name: The name of the corpus.
        :param dataset_name: Return only queries in this dataset.
        :param match: Return only queries matching this.
        :param num_results: How many queries to return.
        :param offset: Offset for pagination.
        :param order_by: In what order to return the queries.
        :param order_by_desc: Whether to order in a descending or ascending fashion.
        :return: Paginated list of queries.
        """
        where_clause = [ORMCorpus.name == corpus_name]
        if dataset_name is not None:
            where_clause.append(ORMDataset.name == dataset_name)
        if match is not None:
            where_clause.append(
                ORMQuery.text.bool_op("@@@")(escape_search_query(match))
            )

        order_by_op = desc if order_by_desc else asc
        if order_by == "relevant_documents":
            order_by_clause = (order_by_op(text("count")), ORMQuery.pkey)
        elif order_by == "length":
            order_by_clause = (
                order_by_op(func.length(ORMQuery.text)),
                ORMQuery.pkey,
            )
        elif order_by == "match_score":
            order_by_clause = (
                order_by_op(func.paradedb.score(ORMQuery.pkey)),
                ORMQuery.pkey,
            )
        else:
            order_by_clause = (ORMQuery.pkey,)

        sql_count = (
            select(func.count())
            .select_from(ORMQuery)
            .join(ORMDataset)
            .join(ORMCorpus)
            .where(*where_clause)
        )

        sql = (
            select(
                ORMQuery.id,
                ORMQuery.text,
                ORMQuery.description,
                func.count()
                .filter(ORMQRel.relevance >= ORMDataset.min_relevance)
                .label("count"),
                ORMDataset.name,
            )
            .select_from(ORMQuery)
            .join(ORMDataset, onclause=ORMQuery.dataset_pkey == ORMDataset.pkey)
            .outerjoin(ORMQRel)
            .join(ORMCorpus, onclause=ORMDataset.corpus_pkey == ORMCorpus.pkey)
            .where(*where_clause)
            .group_by(
                ORMQuery.pkey,
                ORMQuery.id,
                ORMQuery.description,
                ORMQuery.text,
                ORMDataset.name,
            )
            .order_by(*order_by_clause)
            .limit(num_results)
            .offset(offset)
        )

        total_num_results = (await transaction.execute(sql_count)).scalar_one()
        result = (await transaction.execute(sql)).all()
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
        transaction: "AsyncSession",
        corpus_name: str,
        dataset_name: str,
        query_id: str,
    ) -> Query:
        """Return a single specific query.

        :param transaction: A DB transaction.
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
                    ORMQRel.relevance >= ORMDataset.min_relevance
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
            db_query, num_rel_docs = (await transaction.execute(sql)).one()
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
        self, transaction: "AsyncSession", corpus_name: str, document_id: str
    ) -> Document:
        """Return a single specific document.

        :param transaction: A DB transaction.
        :param corpus_name: The corpus name.
        :param document_id: The document ID.
        :raises HTTPException: When the document does not exist.
        :return: The document object.
        """
        sql = (
            select(
                ORMDocument,
                func.count(ORMQRel.query_pkey).filter(
                    ORMQRel.relevance >= ORMDataset.min_relevance
                ),
            )
            .join(ORMCorpus)
            .outerjoin(ORMQRel)
            .outerjoin(ORMQuery)
            .outerjoin(ORMDataset)
            .where(ORMCorpus.name == corpus_name, ORMDocument.id == document_id)
        ).group_by(ORMDocument.pkey)

        try:
            db_document, num_rel_queries = (await transaction.execute(sql)).one()
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
        transaction: "AsyncSession",
        corpus_name: str,
        match: str | None = None,
        num_results: int = 10,
        offset: int = 0,
        order_by: Literal["relevant_queries", "length", "match_score"] | None = None,
        order_by_desc: bool = True,
    ) -> Paginated[Document]:
        """List documents.

        :param transaction: A DB transaction.
        :param corpus_name: The name of the corpus.
        :param match: Return only documents matching this.
        :param num_results: How many documents to return.
        :param offset: Offset for pagination.
        :param order_by: In what order to return the documents.
        :param order_by_desc: Whether to order in a descending or ascending fashion.
        :return: Paginated list of documents.
        """
        # filtering by corpus pkey seems to be faster than filtering by name
        sq_corpus_pkey = (
            select(ORMCorpus.pkey)
            .where(ORMCorpus.name == corpus_name)
            .scalar_subquery()
        )

        where_clause = [ORMDocument.corpus_pkey == sq_corpus_pkey]
        if match is not None:
            where_clause.append(
                ORMDocument.text.bool_op("@@@")(escape_search_query(match))
            )

        # count all matching docoments
        sql_count = select(func.count()).select_from(ORMDocument).where(*where_clause)

        select_clause_sq = [
            ORMDocument.pkey,
            func.count()
            .filter(ORMQRel.relevance >= ORMDataset.min_relevance)
            .label("count"),
        ]

        order_by_op = desc if order_by_desc else asc
        if order_by == "relevant_queries":
            order_by_clause = [order_by_op(text("count"))]
        elif order_by == "length":
            select_clause_sq.append(ORMDocument.text_length.label("text_length"))
            order_by_clause = [order_by_op(text("text_length"))]
        elif order_by == "match_score":
            select_clause_sq.append(
                func.paradedb.score(ORMDocument.pkey).label("score")
            )
            order_by_clause = [order_by_op(text("score"))]
        else:
            order_by_clause = []

        # select pkeys of matching documents in correct order
        sq_document_pkeys = (
            select(*select_clause_sq)
            .outerjoin(ORMQRel)
            .outerjoin(ORMQuery)
            .outerjoin(ORMDataset)
            .where(*where_clause)
            .group_by(ORMDocument.pkey)
            .order_by(*order_by_clause, ORMDocument.pkey)
            .limit(num_results)
            .offset(offset)
        ).subquery()

        # join with full set of documents to get the other columns
        sq_all_docs = select(ORMDocument).subquery()

        select_clause = [
            sq_all_docs.c.id,
            sq_all_docs.c.title,
            sq_all_docs.c.text,
            sq_document_pkeys.c.count,
        ]

        if "text_length" in sq_document_pkeys.c:
            select_clause.append(sq_document_pkeys.c.text_length)
        if "score" in sq_document_pkeys.c:
            select_clause.append(sq_document_pkeys.c.score)
        sql = (
            select(*select_clause)
            .select_from(sq_document_pkeys)
            .join(sq_all_docs, onclause=sq_document_pkeys.c.pkey == sq_all_docs.c.pkey)
            .order_by(*order_by_clause, sq_all_docs.c.pkey)
        )

        total_num_results = (await transaction.execute(sql_count)).scalar_one()
        result = (await transaction.execute(sql)).all()
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
        transaction: "AsyncSession",
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

        :param transaction: A DB transaction.
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
        where_clause = [
            ORMCorpus.name == corpus_name,
            ORMQRel.relevance >= ORMDataset.min_relevance,
        ]
        if document_id is not None:
            where_clause.append(ORMDocument.id == document_id)
        if dataset_name is not None:
            where_clause.append(ORMDataset.name == dataset_name)
        if query_id is not None:
            where_clause.append(ORMQuery.id == query_id)
        if match_query is not None:
            where_clause.append(
                ORMQuery.text.bool_op("@@@")(escape_search_query(match_query))
            )
        if match_document is not None:
            where_clause.append(
                ORMDocument.text.bool_op("@@@")(escape_search_query(match_document))
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
                order_by_op(func.paradedb.score(ORMQuery.pkey)),
                ORMQRel.query_pkey,
                ORMQRel.document_pkey,
            )
        elif order_by == "document_match_score":
            order_by_clause = (
                order_by_op(func.paradedb.score(ORMDocument.pkey)),
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

        total_num_results = (await transaction.execute(sql_count)).scalar_one()
        result = (await transaction.execute(sql)).scalars()
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
