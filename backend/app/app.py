from db import CONFIG
from db.controller import DBController
from litestar import Litestar
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyInitPlugin

app = Litestar(
    route_handlers=[DBController],
    plugins=[SQLAlchemyInitPlugin(CONFIG)],
)
