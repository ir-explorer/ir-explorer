# IR Explorer

> [!IMPORTANT]  
> Early work in progress.

## Planned features

- Display queries, documents, and QRels for IR datasets
- Search within the corpora
- Visualize and compare rankings
- Compute metrics

## Running with Docker

The backend and database can be run easily with Docker:

```bash
docker compose up --watch
```

The backend REST API is made available on port `8000`:

- http://127.0.0.1:8000/schema/
- http://127.0.0.1:8000/schema/swagger

The example script under `scripts/add_dataset.py` may be used to index datasets directly from [ir-datasets](https://ir-datasets.com/).
