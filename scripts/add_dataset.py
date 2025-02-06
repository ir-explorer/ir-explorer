from argparse import ArgumentParser

import ir_datasets
import requests
from tqdm import tqdm

BASE_URL = "http://127.0.0.1:8000"


def main():
    ap = ArgumentParser()
    ap.add_argument("DATASET_NAME", type=str)
    ap.add_argument("CORPUS_NAME", type=str)
    args = ap.parse_args()

    requests.post(BASE_URL + "/add_corpus", json=args.CORPUS_NAME)
    requests.post(
        BASE_URL + "/add_dataset",
        json={"name": args.DATASET_NAME, "corpus_name": args.CORPUS_NAME},
    )

    ds = ir_datasets.load(args.DATASET_NAME)
    for doc in tqdm(ds.docs_iter(), total=ds.docs_count()):
        requests.post(
            BASE_URL + "/add_document",
            json={
                "id": doc.doc_id,
                "corpus_name": args.CORPUS_NAME,
                "title": doc.title,
                "text": doc.text,
            },
        )

    for query in tqdm(ds.queries_iter(), total=ds.queries_count()):
        requests.post(
            BASE_URL + "/add_query",
            json={
                "id": query.query_id,
                "dataset_name": args.DATASET_NAME,
                "text": query.text,
                "description": None,
                "num_relevant_documents": 0,  # TODO: remove
            },
        )

    for qrel in tqdm(ds.qrels_iter(), total=ds.qrels_count()):
        requests.post(
            BASE_URL + "/add_qrel",
            json={
                "query_id": qrel.query_id,
                "dataset_name": args.DATASET_NAME,
                "document_id": qrel.doc_id,
                "corpus_name": args.CORPUS_NAME,
                "relevance": max(1, qrel.relevance),  # TODO: fix
            },
        )


if __name__ == "__main__":
    main()
