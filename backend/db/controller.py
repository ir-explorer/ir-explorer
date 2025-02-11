from typing import TYPE_CHECKING

from litestar import Controller, get, post
from litestar.di import Provide
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from sqlalchemy import and_, func, insert, literal_column, select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import joinedload

from db import provide_transaction
from db.schema import ORMCorpus, ORMDataset, ORMDocument, ORMQRel, ORMQuery
from models import (
    Dataset,
    Document,
    DocumentSearchHit,
    DocumentWithRelevance,
    QRel,
    Query,
    QueryWithRelevanceInfo,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class DBController(Controller):
    """Controller that handles database related API endpoints."""

    dependencies = {"transaction": Provide(provide_transaction)}

    @post(path="/create_corpus")
    async def create_corpus(self, data: str, transaction: "AsyncSession") -> None:
        """Create a new corpus in the database.

        :param data: The corpus name.
        :param transaction: A DB transaction.
        :raises HTTPException: When the corpus cannot be added to the database.
        """
        sql = insert(ORMCorpus).values({"name": data})

        try:
            await transaction.execute(sql)
        except IntegrityError:
            raise HTTPException(
                "Failed to add corpus.",
                status_code=HTTP_409_CONFLICT,
                extra={"corpus_name": data},
            )

    @post(path="/create_dataset")
    async def create_dataset(self, data: Dataset, transaction: "AsyncSession") -> None:
        """Create a new dataset in the database.

        :param data: The dataset.
        :param transaction: A DB transaction.
        :raises HTTPException: When the dataset cannot be added to the database.
        """
        sql = insert(ORMDataset).values(
            {
                "name": data.name,
                "corpus_id": select(ORMCorpus.id).filter_by(name=data.corpus_name),
            }
        )

        try:
            await transaction.execute(sql)
        except IntegrityError:
            raise HTTPException(
                "Failed to add dataset.",
                status_code=HTTP_409_CONFLICT,
                extra=data.__dict__,
            )

    @post(path="/add_query")
    async def add_query(self, data: Query, transaction: "AsyncSession") -> None:
        """Insert a new query into the database.

        :param data: The query to insert.
        :param transaction: A DB transaction.
        :raises HTTPException: When the query cannot be added to the database.
        """
        sql = insert(ORMQuery).values(
            {
                "id": data.id,
                "dataset_id": select(ORMDataset.id)
                .join(ORMCorpus)
                .where(
                    and_(
                        ORMDataset.name == data.dataset_name,
                        ORMCorpus.name == data.corpus_name,
                    )
                ),
                "text": data.text,
                "description": data.description,
            }
        )

        try:
            await transaction.execute(sql)
        except IntegrityError:
            raise HTTPException(
                "Failed to add query.",
                status_code=HTTP_409_CONFLICT,
                extra=data.__dict__,
            )

    @post(path="/add_document")
    async def add_document(self, data: Document, transaction: "AsyncSession") -> None:
        """Insert a new document into the database.

        :param data: The document to insert.
        :param transaction: A DB transaction.
        :raises HTTPException: When the document cannot be added to the database.
        """
        sql = insert(ORMDocument).values(
            {
                "id": data.id,
                "corpus_id": select(ORMCorpus.id).filter_by(name=data.corpus_name),
                "title": data.title,
                "text": data.text,
            }
        )

        try:
            await transaction.execute(sql)
        except IntegrityError:
            raise HTTPException(
                "Failed to add Document.",
                status_code=HTTP_409_CONFLICT,
                extra=data.__dict__,
            )

    @post(path="/add_qrel")
    async def add_qrel(self, data: QRel, transaction: "AsyncSession") -> None:
        """Insert a new query-document relevance into the database.

        :param data: The QRel to insert.
        :param transaction: A DB transaction.
        :raises HTTPException: When the QRel cannot be added to the database.
        """
        sql = insert(ORMQRel).values(
            {
                "query_id": data.query_id,
                "document_id": data.document_id,
                "corpus_id": select(ORMCorpus.id).filter_by(name=data.corpus_name),
                "dataset_id": select(ORMDataset.id)
                .join(ORMCorpus)
                .where(
                    and_(
                        ORMCorpus.name == data.corpus_name,
                        ORMDataset.name == data.dataset_name,
                    )
                ),
                "relevance": data.relevance,
            }
        )

        try:
            await transaction.execute(sql)
        except IntegrityError:
            raise HTTPException(
                "Failed to add QRel.",
                status_code=HTTP_409_CONFLICT,
                extra=data.__dict__,
            )

    @get(path="/get_queries")
    async def get_queries(
        self, corpus_name: str, dataset_name: str, transaction: "AsyncSession"
    ) -> list[QueryWithRelevanceInfo]:
        """List all queries in a dataset.

        :param corpus_name: The name of the corpus.
        :param dataset_name: The dataset name.
        :param transaction: A DB transaction.
        :return: All dataset queries.
        """
        sql = (
            select(ORMQuery, func.count(ORMQRel.document_id))
            .join(ORMDataset)
            .join(ORMCorpus, ORMDataset.corpus_id == ORMCorpus.id)
            .outerjoin(ORMQRel)
            .where(
                and_(
                    ORMCorpus.name == corpus_name,
                    ORMDataset.name == dataset_name,
                )
            )
            .group_by(ORMQuery.id, ORMQuery.dataset_id)
        )
        result = (await transaction.execute(sql)).all()
        return [
            QueryWithRelevanceInfo(
                id=db_query.id,
                corpus_name=corpus_name,
                dataset_name=dataset_name,
                text=db_query.text,
                description=db_query.description,
                num_relevant_documents=num_rel_docs,
            )
            for db_query, num_rel_docs in result
        ]

    @get(path="/get_query")
    async def get_query(
        self,
        corpus_name: str,
        dataset_name: str,
        query_id: str,
        transaction: "AsyncSession",
    ) -> QueryWithRelevanceInfo:
        """Return a single specific query.

        :param corpus_name: The name of the corpus.
        :param dataset_name: The dataset name.
        :param query_id: The query ID.
        :param transaction: A DB transaction.
        :raises HTTPException: When the query does not exist.
        :return: The query object.
        """
        sql = (
            select(ORMQuery, func.count(ORMQRel.document_id))
            .join(ORMDataset)
            .join(ORMCorpus, ORMDataset.corpus_id == ORMCorpus.id)
            .outerjoin(ORMQRel)
            .where(
                and_(
                    ORMQuery.id == query_id,
                    ORMCorpus.name == corpus_name,
                    ORMDataset.name == dataset_name,
                )
            )
            .group_by(ORMQuery.id, ORMQuery.dataset_id)
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

        return QueryWithRelevanceInfo(
            id=db_query.id,
            corpus_name=corpus_name,
            dataset_name=dataset_name,
            text=db_query.text,
            description=db_query.description,
            num_relevant_documents=num_rel_docs,
        )

    @get(path="/get_relevant_documents")
    async def get_relevant_documents(
        self,
        corpus_name: str,
        dataset_name: str,
        query_id: str,
        transaction: "AsyncSession",
    ) -> list[DocumentWithRelevance]:
        """Return all documents that are relevant w.r.t. a specific query.

        :param corpus_name: The name of the corpus.
        :param dataset_name: The name of the dataset the query is in.
        :param query_id: The query ID.
        :param transaction: A DB transaction.
        :return: All documents relevant w.r.t. the query.
        """
        sql = (
            select(ORMQRel)
            .join(ORMDataset, ORMQRel.dataset_id == ORMDataset.id)
            .join(ORMCorpus)
            .options(joinedload(ORMQRel.document))
            .where(
                and_(
                    ORMQRel.query_id == query_id,
                    ORMDataset.name == dataset_name,
                    ORMCorpus.name == corpus_name,
                )
            )
        )

        result = (await transaction.execute(sql)).scalars()

        return [
            DocumentWithRelevance(
                id=qrel.document.id,
                corpus_name=corpus_name,
                title=qrel.document.title,
                text=qrel.document.text,
                query_id=query_id,
                relevance=qrel.relevance,
            )
            for qrel in result
        ]

    @get(path="/get_document")
    async def get_document(
        self, corpus_name: str, document_id: str, transaction: "AsyncSession"
    ) -> Document:
        """Return a single specific document.

        :param corpus_name: The corpus name.
        :param document_id: The document ID.
        :param transaction: A DB transaction.
        :raises HTTPException: When the document does not exist.
        :return: The document object.
        """
        sql = (
            select(ORMDocument)
            .join(ORMCorpus)
            .where(
                and_(
                    ORMDocument.id == document_id,
                    ORMCorpus.name == corpus_name,
                )
            )
        )
        try:
            result = (await transaction.execute(sql)).scalar_one()
        except NoResultFound:
            raise HTTPException(
                "Could not find the requested document.",
                status_code=HTTP_404_NOT_FOUND,
                extra={"document_id": document_id, "corpus_name": corpus_name},
            )
        return Document(result.id, corpus_name, result.title, result.text)

    @get(path="/search_documents")
    async def search_documents(
        self,
        corpus_name: str,
        search: str,
        num_results: int,
        transaction: "AsyncSession",
    ) -> list[DocumentSearchHit]:
        """Search documents within a corpus (using full-text search).

        :param corpus_name: The corpus name.
        :param search: The search string.
        :param num_results: How many documents to return.
        :param transaction: A DB transaction.
        :return: The resulting documents (ordered by score).
        """
        tsv_text = func.to_tsvector(literal_column("'english'"), ORMDocument.text)
        tsv_search = func.websearch_to_tsquery("english", search)
        ts_rank = func.ts_rank_cd(tsv_text, tsv_search)

        sql = (
            select(ORMDocument, ts_rank.label("rank"))
            .join(ORMCorpus)
            .where(
                and_(
                    tsv_text.bool_op("@@")(tsv_search),
                    ORMCorpus.name == corpus_name,
                )
            )
            .order_by("rank")
            .limit(num_results)
        )
        result = (await transaction.execute(sql)).all()

        return [
            DocumentSearchHit(
                id=doc.id,
                corpus_name=corpus_name,
                title=doc.title,
                text=doc.text,
                score=score,
            )
            for doc, score in result
        ]
