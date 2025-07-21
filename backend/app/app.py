import os
from datetime import datetime, timedelta

from db import CONFIG
from db.controller import DBController
from litestar import Litestar, Request
from litestar.config.response_cache import ResponseCacheConfig
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyInitPlugin
from litestar.stores.memory import MemoryStore

CACHE_STORE = MemoryStore()
CACHE_EXPIRATION_DURATION = int(
    os.environ.get("CACHE_EXPIRATION_DURATION", None) or 120
)
CACHE_DELETE_EXPIRED_INTERVAL = int(
    os.environ.get("CACHE_DELETE_EXPIRED_INTERVAL", None) or 600
)


async def before_request(request: Request) -> None:
    """Before-request hook.

    Delete all items from the cache if it has been invalidated

    :param request: The request.
    """
    if request.app.state.get("cache_invalid", False):
        request.logger.info("clearing all items from cache")
        await CACHE_STORE.delete_all()
        request.app.state["cache_invalid"] = False


async def after_response(request: Request) -> None:
    """After-response hook.

    Remove expired items from the cache in a set interval.
    Invalidate the entire cache if data was added or removed in the request.

    :param request: The request.
    """
    route_name = str(request.route_handler).split(".")[-1]
    if (
        route_name.startswith("create")
        or route_name.startswith("add")
        or route_name.startswith("remove")
    ):
        request.logger.info("invalidating cache")
        request.app.state["cache_invalid"] = True

    now = datetime.now()
    if datetime.now() - request.app.state.get(
        "cache_last_delete_expired", now
    ) > timedelta(seconds=CACHE_DELETE_EXPIRED_INTERVAL):
        request.logger.info("clearing expired items from cache")
        await CACHE_STORE.delete_expired()
    request.app.state["cache_last_delete_expired"] = now


app = Litestar(
    route_handlers=[DBController],
    plugins=[SQLAlchemyInitPlugin(CONFIG)],
    stores={"cache": CACHE_STORE},
    # configure caching for successful responses
    response_cache_config=ResponseCacheConfig(
        default_expiration=CACHE_EXPIRATION_DURATION,
        cache_response_filter=lambda _, status_code: 200 <= status_code < 300,
        store="cache",
    ),
    before_request=before_request,
    after_response=after_response,
)
