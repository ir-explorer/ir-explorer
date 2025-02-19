"""Module for database-related functionality."""

import os
from typing import TYPE_CHECKING

from litestar.contrib.sqlalchemy.plugins import SQLAlchemyAsyncConfig
from litestar.exceptions import ClientException
from litestar.status_codes import HTTP_409_CONFLICT
from sqlalchemy import URL
from sqlalchemy.exc import IntegrityError

from db.schema import ORMBase

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from sqlalchemy.ext.asyncio import AsyncSession


async def provide_transaction(
    db_session: "AsyncSession",
) -> "AsyncGenerator[AsyncSession, None]":
    """Provide a database transaction in accordance with SQLAlchemyInitPlugin.

    :param db_session: Asynchronous DB session.
    :raises ClientException: Upon DB integrity errors.
    :yield: The DB transaction.
    """
    try:
        async with db_session.begin():
            yield db_session
    except IntegrityError as exc:
        raise ClientException(
            status_code=HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


CONFIG = SQLAlchemyAsyncConfig(
    connection_string=URL.create(
        drivername="postgresql+asyncpg",
        username=os.environ.get("PG_USER", "pg"),
        password=os.environ.get("PG_PASSWORD", "pg"),
        host=os.environ.get("PG_HOST", "localhost"),
        port=int(os.environ.get("PG_PORT", "5432")),
        database=os.environ.get("PG_DB", "ir-ex"),
    ).__to_string__(hide_password=False),
    metadata=ORMBase.metadata,
    create_all=True,
)
