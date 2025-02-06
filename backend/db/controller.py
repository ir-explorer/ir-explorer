from typing import TYPE_CHECKING

from litestar import Controller, get, post
from litestar.di import Provide
from sqlalchemy import and_, func, select
from sqlalchemy.orm import joinedload

from db import provide_transaction
from db.schema import ORMDocument, ORMQRel, ORMQuery
from models import Document, QRel, Query, RelevantDocument

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class DBController(Controller):
    """Controller that handles database related API endpoints."""

    dependencies = {"transaction": Provide(provide_transaction)}

    @get(path="/list_queries")
    async def list_queries(
        self, dataset_name: str, transaction: "AsyncSession"
    ) -> list[Query]:
        """List all queries in a dataset.

        :param dataset_name: The dataset name.
        :param transaction: A DB transaction.
        :return: All dataset queries.
        """
        result = (
            await transaction.execute(
                select(ORMQuery, func.count(ORMQRel.document_id))
                .outerjoin(ORMQRel)
                .where(ORMQuery.dataset_name == dataset_name)
                .group_by(ORMQuery.id, ORMQuery.dataset_name)
            )
        ).all()
        return [
            Query(
                db_query.id,
                db_query.dataset_name,
                db_query.text,
                db_query.description,
                num_rel_docs,
            )
            for db_query, num_rel_docs in result
        ]

    @get(path="/get_query")
    async def get_query(
        self, dataset_name: str, query_id: str, transaction: "AsyncSession"
    ) -> Query:
        """Return a single specific query.

        :param dataset_name: The dataset name.
        :param query_id: The query ID.
        :param transaction: A DB transaction.
        :return: The query object.
        """
        db_query, num_rel_docs = (
            await transaction.execute(
                select(ORMQuery, func.count(ORMQRel.document_id))
                .outerjoin(ORMQRel)
                .where(
                    and_(ORMQuery.id == query_id, ORMQuery.dataset_name == dataset_name)
                )
                .group_by(ORMQuery.id, ORMQuery.dataset_name)
            )
        ).one()
        return Query(
            db_query.id,
            db_query.dataset_name,
            db_query.text,
            db_query.description,
            num_rel_docs,
        )

    @get(path="/get_relevant_documents")
    async def get_relevant_documents(
        self, dataset_name: str, query_id: str, transaction: "AsyncSession"
    ) -> list[RelevantDocument]:
        """Return all documents that a relevant w.r.t. a specific query.

        :param dataset_name: The name of the dataset the query is in.
        :param query_id: The query ID.
        :param transaction: A DB transaction.
        :return: All documents relevant w.r.t. the query.
        """
        sql = (
            select(ORMQRel)
            .options(joinedload(ORMQRel.document))
            .where(
                and_(ORMQRel.query_id == query_id, ORMQRel.dataset_name == dataset_name)
            )
        )
        result = (await transaction.execute(sql)).scalars()
        return [
            RelevantDocument(
                qrel.document.id,
                qrel.document.corpus_name,
                qrel.document.title,
                qrel.document.text,
                qrel.relevance,
            )
            for qrel in result
        ]

    @post(path="/add_query")
    async def add_query(self, data: Query, transaction: "AsyncSession") -> Query:
        """Insert a new query into the database.

        :param data: The query to insert.
        :param transaction: A DB transaction.
        :return: The inserted query.
        """
        transaction.add(
            ORMQuery(
                id=data.id,
                dataset_name=data.dataset_name,
                text=data.text,
                description=data.description,
            )
        )
        return data

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
        sql = select(ORMDocument).where(
            and_(ORMDocument.id == document_id, ORMDocument.corpus_name == corpus_name)
        )
        result = (await transaction.execute(sql)).scalar_one()
        return Document(result.id, result.corpus_name, result.title, result.text)

    @post(path="/add_document")
    async def add_document(
        self, data: Document, transaction: "AsyncSession"
    ) -> Document:
        """Insert a new document into the database.

        :param data: The document to insert.
        :param transaction: A DB transaction.
        :return: The inserted document.
        """
        transaction.add(
            ORMDocument(
                id=data.id,
                corpus_name=data.corpus_name,
                title=data.title,
                text=data.text,
            )
        )
        return data

    @post(path="/add_qrel")
    async def add_qrel(self, data: QRel, transaction: "AsyncSession") -> QRel:
        """Insert a new query-document relevance into the database.

        :param data: The QRel to insert.
        :param transaction: A DB transaction.
        :return: The inserted QRel.
        """
        transaction.add(
            ORMQRel(
                query_id=data.query_id,
                dataset_name=data.dataset_name,
                document_id=data.document_id,
                corpus_name=data.corpus_name,
                relevance=data.relevance,
            )
        )
        return data
