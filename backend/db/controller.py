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
    BulkDocument,
    BulkQRel,
    BulkQuery,
    Corpus,
    Dataset,
    Document,
    DocumentSearchHit,
    DocumentWithRelevance,
    QueryWithRelevanceInfo,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.ext.asyncio import AsyncSession


class DBController(Controller):
    """Controller that handles database related API endpoints."""

    dependencies = {"transaction": Provide(provide_transaction)}

    @post(path="/create_corpus")
    async def create_corpus(self, transaction: "AsyncSession", data: Corpus) -> None:
        """Create a new corpus in the database.

        :param transaction: A DB transaction.
        :param data: The corpus.
        :raises HTTPException: When the corpus cannot be added to the database.
        """
        sql = insert(ORMCorpus).values({"name": data.name, "language": data.language})

        try:
            await transaction.execute(sql)
        except IntegrityError as e:
            raise HTTPException(
                "Failed to add corpus.",
                status_code=HTTP_409_CONFLICT,
                extra={"corpus_name": data.name, "code": e.code},
            )

    @post(path="/create_dataset")
    async def create_dataset(self, transaction: "AsyncSession", data: Dataset) -> None:
        """Create a new dataset in the database.

        :param transaction: A DB transaction.
        :param data: The dataset.
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
        except IntegrityError as e:
            raise HTTPException(
                "Failed to add dataset.",
                status_code=HTTP_409_CONFLICT,
                extra={
                    "name": data.name,
                    "corpus_name": data.corpus_name,
                    "code": e.code,
                },
            )

    @post(path="/add_queries")
    async def add_queries(
        self,
        transaction: "AsyncSession",
        dataset_name: str,
        corpus_name: str,
        data: "Sequence[BulkQuery]",
    ) -> None:
        """Insert new queries into the database.

        :param transaction: A DB transaction.
        :param dataset_name: The dataset the queries belong to.
        :param corpus_name: The corpus the dataset belongs to.
        :param data: The queries to insert.
        :raises HTTPException: When the queries cannot be added to the database.
        """
        dataset_cte = (
            select(ORMDataset)
            .join(ORMCorpus)
            .where(
                and_(
                    ORMDataset.name == dataset_name,
                    ORMCorpus.name == corpus_name,
                )
            )
        ).cte()
        sql = insert(ORMQuery).values(
            [
                {
                    "id": q.id,
                    "dataset_id": select(dataset_cte.c.id),
                    "text": q.text,
                    "description": q.description,
                }
                for q in data
            ]
        )

        try:
            await transaction.execute(sql)
        except IntegrityError as e:
            raise HTTPException(
                "Failed to add queries.",
                status_code=HTTP_409_CONFLICT,
                extra={"code": e.code},
            )

    @post(path="/add_documents")
    async def add_documents(
        self,
        transaction: "AsyncSession",
        corpus_name: str,
        data: "Sequence[BulkDocument]",
    ) -> None:
        """Insert new documents into the database.

        :param transaction: A DB transaction.
        :param corpus_name: The corpus the documents belong to.
        :param data: The documents to insert.
        :raises HTTPException: When the documents cannot be added to the database.
        """
        corpus_cte = (select(ORMCorpus).where(ORMCorpus.name == corpus_name)).cte()
        sql = insert(ORMDocument).values(
            [
                {
                    "id": doc.id,
                    "corpus_id": select(corpus_cte.c.id),
                    "title": doc.title,
                    "text": doc.text,
                }
                for doc in data
            ]
        )

        try:
            await transaction.execute(sql)
        except IntegrityError as e:
            raise HTTPException(
                "Failed to add Documents.",
                status_code=HTTP_409_CONFLICT,
                extra={"code": e.code},
            )

    @post(path="/add_qrels")
    async def add_qrels(
        self,
        transaction: "AsyncSession",
        dataset_name: str,
        corpus_name: str,
        data: "Sequence[BulkQRel]",
    ) -> None:
        """Insert QRels into the database.

        :param transaction: A DB transaction.
        :param dataset_name: The dataset the QRels belong to.
        :param corpus_name: The corpus the dataset belongs to.
        :param data: The QRels to insert.
        :raises HTTPException: When the QRels cannot be added to the database.
        """
        dataset_cte = (
            select(ORMDataset)
            .join(ORMCorpus)
            .where(
                and_(
                    ORMDataset.name == dataset_name,
                    ORMCorpus.name == corpus_name,
                )
            )
        ).cte()
        sql = insert(ORMQRel).values(
            [
                {
                    "query_id": qrel.query_id,
                    "document_id": qrel.document_id,
                    "corpus_id": select(dataset_cte.c.corpus_id),
                    "dataset_id": select(dataset_cte.c.id),
                    "relevance": qrel.relevance,
                }
                for qrel in data
            ]
        )

        try:
            await transaction.execute(sql)
        except IntegrityError as e:
            raise HTTPException(
                "Failed to add QRels.",
                status_code=HTTP_409_CONFLICT,
                extra={"code": e.code},
            )

    @get(path="/get_corpora")
    async def get_corpora(self, transaction: "AsyncSession") -> list[Corpus]:
        """List all corpora.

        :param transaction: A DB transaction.
        :return: All corpora.
        """
        sql = select(ORMCorpus)
        result = (await transaction.execute(sql)).scalars().all()
        return [
            Corpus(
                name=corpus.name,
                language=corpus.language,
            )
            for corpus in result
        ]

    @get(path="/get_datasets")
    async def get_datasets(
        self, transaction: "AsyncSession", corpus_name: str
    ) -> list[Dataset]:
        """List all datasets for a corpus.

        :param transaction: A DB transaction.
        :param corpus_name: The name of the corpus.
        :return: All datasets.
        """
        sql = (
            select(ORMDataset)
            .join(ORMCorpus, ORMDataset.corpus_id == ORMCorpus.id)
            .where(ORMCorpus.name == corpus_name)
        )
        result = (await transaction.execute(sql)).scalars().all()
        return [
            Dataset(
                name=dataset.name,
                corpus_name=corpus_name,
            )
            for dataset in result
        ]

    @get(path="/get_queries")
    async def get_queries(
        self, transaction: "AsyncSession", corpus_name: str, dataset_name: str
    ) -> list[QueryWithRelevanceInfo]:
        """List all queries in a dataset.

        :param transaction: A DB transaction.
        :param corpus_name: The name of the corpus.
        :param dataset_name: The dataset name.
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
        transaction: "AsyncSession",
        corpus_name: str,
        dataset_name: str,
        query_id: str,
    ) -> QueryWithRelevanceInfo:
        """Return a single specific query.

        :param transaction: A DB transaction.
        :param corpus_name: The name of the corpus.
        :param dataset_name: The dataset name.
        :param query_id: The query ID.
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
        transaction: "AsyncSession",
        corpus_name: str,
        dataset_name: str,
        query_id: str,
    ) -> list[DocumentWithRelevance]:
        """Return all documents that are relevant w.r.t. a specific query.

        :param transaction: A DB transaction.
        :param corpus_name: The name of the corpus.
        :param dataset_name: The name of the dataset the query is in.
        :param query_id: The query ID.
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
        except NoResultFound as e:
            raise HTTPException(
                "Could not find the requested document.",
                status_code=HTTP_404_NOT_FOUND,
                extra={
                    "document_id": document_id,
                    "corpus_name": corpus_name,
                    "code": e.code,
                },
            )
        return Document(result.id, corpus_name, result.title, result.text)

    @get(path="/search_documents")
    async def search_documents(
        self,
        transaction: "AsyncSession",
        corpus_name: str,
        search: str,
        num_results: int = 10,
    ) -> list[DocumentSearchHit]:
        """Search documents within a corpus (using full-text search).

        :param transaction: A DB transaction.
        :param corpus_name: The corpus name.
        :param search: The search string.
        :param num_results: How many documents to return.
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
