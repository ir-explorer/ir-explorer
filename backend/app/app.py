from litestar import Litestar
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyInitPlugin

from db import CONFIG
from db.controller import DBController

app = Litestar(
    route_handlers=[DBController],
    plugins=[SQLAlchemyInitPlugin(CONFIG)],
)
