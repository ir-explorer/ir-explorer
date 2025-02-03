from litestar import Litestar
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyInitPlugin

from db import CONFIG
from db.controller import PostgresController

app = Litestar(
    route_handlers=[PostgresController],
    plugins=[SQLAlchemyInitPlugin(CONFIG)],
)
