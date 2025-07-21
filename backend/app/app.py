import os
from datetime import datetime, timedelta

from db import CONFIG
from db.controller import DBController
from litestar import Litestar, Request
from litestar.config.response_cache import ResponseCacheConfig
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyInitPlugin
from litestar.stores.memory import MemoryStore

CACHE_STORE = MemoryStore()
CACHE_DEFAULT_EXPIRATION = int(os.environ.get("CACHE_DEFAULT_EXPIRATION", None) or 120)
CACHE_CLEAR_INTERVAL = int(os.environ.get("CACHE_CLEAR_INTERVAL", None) or 600)


async def after_response(request: Request) -> None:
    """After-response hook.

    Remove expired items from the cache in a set interval.

    :param request: The request.
    """
    now = datetime.now()
    last_cleared = request.app.state.get("cache_last_cleared", now)
    if datetime.now() - last_cleared > timedelta(seconds=CACHE_CLEAR_INTERVAL):
        await CACHE_STORE.delete_expired()
    app.state["cache_last_cleared"] = now


app = Litestar(
    route_handlers=[DBController],
    plugins=[SQLAlchemyInitPlugin(CONFIG)],
    stores={"cache": CACHE_STORE},
    # configure caching for successful responses
    response_cache_config=ResponseCacheConfig(
        default_expiration=CACHE_DEFAULT_EXPIRATION,
        cache_response_filter=lambda _, status_code: 200 <= status_code < 300,
        store="cache",
    ),
    after_response=after_response,
)
