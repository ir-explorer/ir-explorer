# !/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["ir_datasets", "requests", "tqdm"]
# ///

from argparse import ArgumentParser
from itertools import batched

import ir_datasets
import requests
from tqdm import tqdm


def main():
    ap = ArgumentParser()
    ap.add_argument("DATASET_ID", type=str)
    ap.add_argument("DATASET_NAME", type=str)
    ap.add_argument("CORPUS_NAME", type=str)
    ap.add_argument("--batch_size", type=int, default=2**10)
    ap.add_argument("--language", default="English")
    ap.add_argument("--min_relevance", type=int, default=1)
    ap.add_argument("--add_corpus", action="store_true")
    ap.add_argument("--hostname", default="localhost")
    ap.add_argument("--port", type=int, default=8103)
    ap.add_argument("--text_attr", default="text")
    args = ap.parse_args()

    backend_url = f"http://{args.hostname}:{args.port}"

    ds = ir_datasets.load(args.DATASET_ID)

    if args.add_corpus:
        requests.post(
            backend_url + "/create_corpus",
            json={"name": args.CORPUS_NAME, "language": args.language},
        )
        for batch in tqdm(
            batched(ds.docs_iter(), args.batch_size),
            total=int(ds.docs_count() / args.batch_size) + 1,
            desc="Adding documents",
        ):
            requests.post(
                backend_url + "/add_documents",
                json=[
                    {
                        "id": doc.doc_id,
                        "title": getattr(doc, "title", None),
                        "text": getattr(doc, args.text_attr),
                    }
                    for doc in batch
                ],
                params={"corpus_name": args.CORPUS_NAME},
            )

    requests.post(
        backend_url + "/create_dataset",
        json={
            "name": args.DATASET_NAME,
            "corpus_name": args.CORPUS_NAME,
            "min_relevance": args.min_relevance,
        },
    )

    for batch in tqdm(
        batched(ds.queries_iter(), args.batch_size),
        total=int(ds.queries_count() / args.batch_size) + 1,
        desc="Adding queries",
    ):
        requests.post(
            backend_url + "/add_queries",
            json=[
                {
                    "id": query.query_id,
                    "text": query.text,
                    "description": None,
                }
                for query in batch
            ],
            params={"corpus_name": args.CORPUS_NAME, "dataset_name": args.DATASET_NAME},
        )

    for batch in tqdm(
        batched(ds.qrels_iter(), args.batch_size),
        total=int(ds.qrels_count() / args.batch_size) + 1,
        desc="Adding QRels",
    ):
        requests.post(
            backend_url + "/add_qrels",
            json=[
                {
                    "query_id": qrel.query_id,
                    "document_id": qrel.doc_id,
                    "relevance": qrel.relevance,
                }
                for qrel in batch
            ],
            params={"corpus_name": args.CORPUS_NAME, "dataset_name": args.DATASET_NAME},
        )


if __name__ == "__main__":
    main()
