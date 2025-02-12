from argparse import ArgumentParser
from itertools import batched

import ir_datasets
import requests
from tqdm import tqdm

BASE_URL = "http://127.0.0.1:8000"


def main():
    ap = ArgumentParser()
    ap.add_argument("DATASET_NAME", type=str)
    ap.add_argument("CORPUS_NAME", type=str)
    ap.add_argument("--batch_size", type=int, default=2**10)
    args = ap.parse_args()

    requests.post(BASE_URL + "/create_corpus", json=args.CORPUS_NAME)
    requests.post(
        BASE_URL + "/create_dataset",
        json={"name": args.DATASET_NAME, "corpus_name": args.CORPUS_NAME},
    )

    ds = ir_datasets.load(args.DATASET_NAME)
    for batch in tqdm(
        batched(ds.docs_iter(), args.batch_size),
        total=int(ds.docs_count() / args.batch_size) + 1,
    ):
        requests.post(
            BASE_URL + "/add_documents",
            json=[
                {
                    "id": doc.doc_id,
                    "title": getattr(doc, "title", None),
                    "text": doc.text,
                }
                for doc in batch
            ],
            params={"corpus_name": args.CORPUS_NAME},
        )

    for batch in tqdm(
        batched(ds.queries_iter(), args.batch_size),
        total=int(ds.queries_count() / args.batch_size) + 1,
    ):
        requests.post(
            BASE_URL + "/add_queries",
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
    ):
        requests.post(
            BASE_URL + "/add_qrels",
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
