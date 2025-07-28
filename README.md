# IR Explorer

> [!IMPORTANT]  
> Early work in progress.

## Planned features

- Display queries, documents, and QRels for IR datasets
- Search within the corpora
- Visualize and compare rankings
- Compute metrics

## Running with Docker

The application can easily be run with Docker. For example, spin up a development instance as follows:

```bash
docker compose -f compose.yaml -f compose.dev.yaml up --build --watch
```

The frontend can then be accessed via port `8104`:

- http://127.0.0.1:8104

The backend REST API is available on port `8103`:

- http://127.0.0.1:8103/schema/
- http://127.0.0.1:8103/schema/swagger

The example script under `scripts/add_dataset.py` may be used to index datasets directly from [ir-datasets](https://ir-datasets.com/).
