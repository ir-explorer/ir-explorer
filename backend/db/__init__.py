import os
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from litestar.exceptions import ClientException
from litestar.status_codes import HTTP_409_CONFLICT
from sqlalchemy import Column, ForeignKeyConstraint, Integer, Table
from sqlalchemy.engine import URL
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from litestar import Litestar
    from litestar.datastructures import State


class Base(DeclarativeBase):
    pass


qrels_table = Table(
    "qrels",
    Base.metadata,
    Column("query_id"),
    Column("dataset"),
    Column("document_id"),
    Column("corpus"),
    ForeignKeyConstraint(["query_id", "dataset"], ["queries.id", "queries.dataset"]),
    ForeignKeyConstraint(
        ["document_id", "corpus"], ["documents.id", "documents.corpus"]
    ),
    Column("relevance", Integer()),
)


class Query(Base):
    __tablename__ = "queries"
    id: Mapped[str] = mapped_column(primary_key=True)
    dataset: Mapped[str] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)
    relevant_documents: Mapped[list["Document"]] = relationship(secondary=qrels_table)


class Document(Base):
    __tablename__ = "documents"
    id: Mapped[str] = mapped_column(primary_key=True)
    corpus: Mapped[str] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column()
    title: Mapped[str] = mapped_column(nullable=True)


@asynccontextmanager
async def db_connection(app: "Litestar") -> "AsyncGenerator[None, None]":
    engine = getattr(app.state, "engine", None)
    if engine is None:
        engine = create_async_engine(
            URL.create(
                drivername="postgresql+asyncpg",
                username=os.environ.get("PG_USER", "pg"),
                password=os.environ.get("PG_PASSWORD", "pg"),
                host=os.environ.get("PG_HOST", "localhost"),
                port=int(os.environ.get("PG_PORT", "5432")),
                database=os.environ.get("PG_DB", "ir-ex"),
            )
        )
        app.state.engine = engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield
    finally:
        await engine.dispose()


sessionmaker = async_sessionmaker(expire_on_commit=False)


async def provide_transaction(state: "State") -> "AsyncGenerator[AsyncSession, None]":
    async with sessionmaker(bind=state.engine) as session:
        try:
            async with session.begin():
                yield session

        except IntegrityError as exc:
            raise ClientException(
                status_code=HTTP_409_CONFLICT,
                detail=str(exc),
            ) from exc
