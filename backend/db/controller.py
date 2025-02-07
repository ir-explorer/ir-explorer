from typing import TYPE_CHECKING

from litestar import Controller, get, post
from litestar.di import Provide
from sqlalchemy import and_, func, insert, select
from sqlalchemy.orm import joinedload

from db import provide_transaction
from db.schema import ORMCorpus, ORMDataset, ORMDocument, ORMQRel, ORMQuery
from models import Dataset, Document, QRel, Query, RelevantDocument

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
        """
        transaction.add(ORMCorpus(name=data))

    @post(path="/create_dataset")
    async def create_dataset(self, data: Dataset, transaction: "AsyncSession") -> None:
        """Create a new dataset in the database.

        :param data: The dataset.
        :param transaction: A DB transaction.
        """
        await transaction.execute(
            insert(ORMDataset).values(
                {
                    "name": data.name,
                    "corpus_id": select(ORMCorpus.id).filter_by(name=data.corpus_name),
                }
            )
        )

    @post(path="/add_query")
    async def add_query(self, data: Query, transaction: "AsyncSession") -> None:
        """Insert a new query into the database.

        :param data: The query to insert.
        :param transaction: A DB transaction.
        """
        await transaction.execute(
            insert(ORMQuery).values(
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
        )

    @post(path="/add_document")
    async def add_document(self, data: Document, transaction: "AsyncSession") -> None:
        """Insert a new document into the database.

        :param data: The document to insert.
        :param transaction: A DB transaction.
        """
        await transaction.execute(
            insert(ORMDocument).values(
                {
                    "id": data.id,
                    "corpus_id": select(ORMCorpus.id).filter_by(name=data.corpus_name),
                    "title": data.title,
                    "text": data.text,
                }
            )
        )

    @post(path="/add_qrel")
    async def add_qrel(self, data: QRel, transaction: "AsyncSession") -> None:
        """Insert a new query-document relevance into the database.

        :param data: The QRel to insert.
        :param transaction: A DB transaction.
        """
        await transaction.execute(
            insert(ORMQRel).values(
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
        )

    @get(path="/list_queries")
    async def list_queries(
        self, corpus_name: str, dataset_name: str, transaction: "AsyncSession"
    ) -> list[Query]:
        """List all queries in a dataset.

        :param corpus_name: The name of the corpus.
        :param dataset_name: The dataset name.
        :param transaction: A DB transaction.
        :return: All dataset queries.
        """
        result = (
            await transaction.execute(
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
        ).all()
        return [
            Query(
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
    ) -> Query:
        """Return a single specific query.

        :param corpus_name: The name of the corpus.
        :param dataset_name: The dataset name.
        :param query_id: The query ID.
        :param transaction: A DB transaction.
        :return: The query object.
        """
        db_query, num_rel_docs = (
            await transaction.execute(
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
        ).one()
        return Query(
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
    ) -> list[RelevantDocument]:
        """Return all documents that a relevant w.r.t. a specific query.

        :param corpus_name: The name of the corpus.
        :param dataset_name: The name of the dataset the query is in.
        :param query_id: The query ID.
        :param transaction: A DB transaction.
        :return: All documents relevant w.r.t. the query.
        """
        result = (
            await transaction.execute(
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
        ).scalars()
        return [
            RelevantDocument(
                qrel.document.id,
                corpus_name,
                qrel.document.title,
                qrel.document.text,
                qrel.relevance,
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
        :return: The document object.
        """
        result = (
            await transaction.execute(
                select(ORMDocument)
                .join(ORMCorpus)
                .where(
                    and_(
                        ORMDocument.id == document_id,
                        ORMCorpus.name == corpus_name,
                    )
                )
            )
        ).scalar_one()
        return Document(result.id, corpus_name, result.title, result.text)
