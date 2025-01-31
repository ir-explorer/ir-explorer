from litestar import Litestar
from litestar.contrib.sqlalchemy.plugins import SQLAlchemySerializationPlugin

from db import db_connection, provide_transaction
from db.data import PostgresDataStore

app = Litestar(
    route_handlers=[PostgresDataStore],
    dependencies={"transaction": provide_transaction},
    lifespan=[db_connection],
    plugins=[SQLAlchemySerializationPlugin()],
)
