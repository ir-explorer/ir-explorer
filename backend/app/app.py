import os
from datetime import datetime, timedelta

from db import CONFIG
from db.controller import DBController
from litestar import Litestar, Request, get
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
        request.logger.info("clearing all items from cache")
        await CACHE_STORE.delete_all()
        return

    now = datetime.now()
    if datetime.now() - request.app.state.get(
        "cache_last_delete_expired", datetime.min
    ) > timedelta(seconds=CACHE_DELETE_EXPIRED_INTERVAL):
        request.logger.info("clearing expired items from cache")
        await CACHE_STORE.delete_expired()
        request.app.state["cache_last_delete_expired"] = now


@get(path="/ready")
def ready() -> bool:
    """Perform a simple health check.

    :return: True once the app is ready.
    """
    return True


app = Litestar(
    route_handlers=[DBController, ready],
    plugins=[SQLAlchemyInitPlugin(CONFIG)],
    stores={"cache": CACHE_STORE},
    # configure caching for successful responses
    response_cache_config=ResponseCacheConfig(
        default_expiration=CACHE_EXPIRATION_DURATION,
        cache_response_filter=lambda _, status_code: 200 <= status_code < 300,
        store="cache",
    ),
    after_response=after_response,
)
