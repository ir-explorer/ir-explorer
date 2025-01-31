from litestar import Controller, get, post
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession  # noqa: TC002

from db import Document, Query


class PostgresDataStore(Controller):
    @get(path="/list_queries")
    async def list_queries(
        self, dataset: str, transaction: AsyncSession
    ) -> list[Query]:
        sql = select(Query).where(Query.dataset == dataset).order_by(Query.id)
        sql_result = await transaction.execute(sql)
        return list(sql_result.scalars().all())

    @get(path="/get_query")
    async def get_query(
        self, dataset: str, q_id: str, transaction: AsyncSession
    ) -> Query | None:
        sql = select(Query).where(and_(Query.id == q_id, Query.dataset == dataset))
        sql_result = await transaction.execute(sql)
        return sql_result.scalar()

    @post(path="/add_query")
    async def add_query(self, data: Query, transaction: AsyncSession) -> Query:
        transaction.add(data)
        return data

    @get(path="/get_document")
    async def get_document(
        self, corpus: str, doc_id: str, transaction: AsyncSession
    ) -> Document | None:
        sql = select(Document).where(
            and_(Document.id == doc_id, Document.corpus == corpus)
        )
        sql_result = await transaction.execute(sql)
        return sql_result.scalar()

    @post(path="/add_document")
    async def add_document(self, data: Document, transaction: AsyncSession) -> Document:
        transaction.add(data)
        return data
