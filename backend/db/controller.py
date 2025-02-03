from litestar import Controller, get, post
from litestar.di import Provide
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession  # noqa: TC002
from sqlalchemy.orm import joinedload

from db import provide_transaction
from db.schema import ORMDocument, ORMQRel, ORMQuery
from models import Document, Query, RelevantDocument


class DBController(Controller):
    dependencies = {"transaction": Provide(provide_transaction)}

    @get(path="/list_queries")
    async def list_queries(
        self, dataset: str, transaction: AsyncSession
    ) -> list[Query]:
        result = (
            await transaction.execute(
                select(ORMQuery, func.count(ORMQRel.document_id))
                .outerjoin(ORMQuery.qrels)
                .where(ORMQuery.dataset == dataset)
                .group_by(ORMQuery.id, ORMQuery.dataset)
            )
        ).all()
        return [
            Query(
                db_query.id,
                db_query.dataset,
                db_query.text,
                db_query.description,
                num_rel_docs,
            )
            for db_query, num_rel_docs in result
        ]

    @get(path="/get_query")
    async def get_query(
        self, dataset: str, query_id: str, transaction: AsyncSession
    ) -> Query:
        db_query, num_rel_docs = (
            await transaction.execute(
                select(ORMQuery, func.count(ORMQRel.document_id))
                .outerjoin(ORMQuery.qrels)
                .where(and_(ORMQuery.id == query_id, ORMQuery.dataset == dataset))
                .group_by(ORMQuery.id, ORMQuery.dataset)
            )
        ).one()
        return Query(
            db_query.id,
            db_query.dataset,
            db_query.text,
            db_query.description,
            num_rel_docs,
        )

    @get(path="/get_relevant_documents")
    async def get_relevant_documents(
        self, dataset: str, query_id: str, transaction: AsyncSession
    ) -> list[RelevantDocument]:
        sql = (
            select(ORMQRel)
            .options(joinedload(ORMQRel.document))
            .where(and_(ORMQRel.query_id == query_id, ORMQRel.dataset == dataset))
        )
        result = (await transaction.execute(sql)).scalars()
        return [
            RelevantDocument(
                qrel.document.id,
                qrel.document.corpus,
                qrel.document.title,
                qrel.document.text,
                qrel.relevance,
            )
            for qrel in result
        ]

    @post(path="/add_query")
    async def add_query(self, data: Query, transaction: AsyncSession) -> Query:
        transaction.add(
            ORMQuery(
                id=data.id,
                dataset=data.dataset,
                text=data.text,
                description=data.description,
            )
        )
        return data

    @get(path="/get_document")
    async def get_document(
        self, corpus: str, doc_id: str, transaction: AsyncSession
    ) -> Document:
        sql = select(ORMDocument).where(
            and_(ORMDocument.id == doc_id, ORMDocument.corpus == corpus)
        )
        result = (await transaction.execute(sql)).scalar_one()
        return Document(result.id, result.corpus, result.title, result.text)

    @post(path="/add_document")
    async def add_document(self, data: Document, transaction: AsyncSession) -> Document:
        transaction.add(
            ORMDocument(
                id=data.id, corpus=data.corpus, title=data.title, text=data.text
            )
        )
        return data
