# IR Explorer Backend

The backend is based on [Litestar](https://litestar.dev/), [SQLAlchemy](https://www.sqlalchemy.org/), and [asyncpg](https://magicstack.github.io/asyncpg/current/).

In order to run the backend locally, install [uv](https://docs.astral.sh/uv/) and run:

- `uv sync`
- `uv run litestar --app-dir app run`

For database connectivity, the app reads the following environment variables:

- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `POSTGRES_DB`

Caching can be configured using:

- `CACHE_EXPIRATION_DURATION`: The number of seconds backend responses are cached.
- `CACHE_DELETE_EXPIRED_INTERVAL`: The interval in seconds to delete expired items from the cache.
