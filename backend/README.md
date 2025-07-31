# IR Explorer Backend

The backend is based on [Litestar](https://litestar.dev/), [SQLAlchemy](https://www.sqlalchemy.org/), and [asyncpg](https://magicstack.github.io/asyncpg/current/).

In order to run the backend locally, install [uv](https://docs.astral.sh/uv/) and run:

- `uv sync`
- `uv run litestar --app-dir app run`

The app requires the following environment variables to be set:

- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `POSTGRES_DB`
- `CACHE_EXPIRATION_DURATION`: The number of seconds backend responses are cached.
- `CACHE_DELETE_EXPIRED_INTERVAL`: The interval in seconds to delete expired items from the cache.
