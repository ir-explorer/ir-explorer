from litestar import Litestar
from litestar.contrib.sqlalchemy.plugins import SQLAlchemySerializationPlugin

from db import db_connection
from db.data import PostgresDataStore

app = Litestar(
    route_handlers=[PostgresDataStore],
    lifespan=[db_connection],
    plugins=[SQLAlchemySerializationPlugin()],
)
