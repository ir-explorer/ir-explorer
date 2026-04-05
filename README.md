# IR Explorer

## Planned features

- Display queries, documents, and QRels for IR datasets
- Search within the corpora
- Visualize and compare rankings
- Compute metrics

## Development

Each component ([`backend`](backend/), [`frontend`](frontend/), [`tests`](tests/)) contains a readme file with instructions.

To index datasets directly from [ir-datasets](https://ir-datasets.com/), use the [indexer utility](https://github.com/ir-explorer/indexer).

## With Docker

The application can be run and developed with Docker. For example, spin up a development instance as follows:

```bash
docker compose -f compose.yaml -f compose.dev.yaml up --build --watch
```

The frontend can then be accessed via port `8104`:

- http://127.0.0.1:8104

The backend REST API is available on port `8103`:

- http://127.0.0.1:8103/schema/
- http://127.0.0.1:8103/schema/swagger


## Devcontainers

Devcontainer configurations are available in [`.devcontainer`](.devcontainer/) and can be used for development and testing.