from fastapi import FastAPI

from data import TestDataStore

app = FastAPI()
ds = TestDataStore()


app.add_api_route("/available_datasets", ds.available_datasets, methods=["GET"])
app.add_api_route("/available_corpora", ds.available_corpora, methods=["GET"])
app.add_api_route("/list_queries/{dataset:path}", ds.list_queries, methods=["GET"])
app.add_api_route("/list_documents/{dataset:path}", ds.list_documents, methods=["GET"])
app.add_api_route("/get_query/{dataset:path}/{q_id}", ds.get_query, methods=["GET"])
app.add_api_route(
    "/get_document/{dataset:path}/{doc_id}", ds.get_document, methods=["GET"]
)
