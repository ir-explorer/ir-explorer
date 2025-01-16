from abc import ABC, abstractmethod

import ir_datasets
from fastapi import HTTPException
from pydantic import BaseModel


class CorpusDescription(BaseModel):
    name: str
    num_documents: int
    searchers: list[str] = []


class DatasetDescription(BaseModel):
    name: str
    corpus: str
    num_queries: int
    num_qrels: int = 0


class Query(BaseModel):
    id: str
    text: str
    description: str | None = None
    metadata: dict[str, str] = {}


class Document(BaseModel):
    id: str
    text: str
    title: str | None = None
    metadata: dict[str, str] = {}


class SearchHit(BaseModel):
    document_id: str
    score: float | None


class SearchResult(BaseModel):
    query: str
    query_id: str | None = None
    result: list[SearchHit]


class DataStore(ABC):
    @abstractmethod
    def available_corpora(self) -> list[CorpusDescription]:
        pass

    @abstractmethod
    def available_datasets(self) -> list[DatasetDescription]:
        pass

    @abstractmethod
    def list_queries(self, dataset: str, start_index: int, num: int) -> list[Query]:
        pass

    @abstractmethod
    def list_documents(self, corpus: str, start_index: int, num: int) -> list[Document]:
        pass

    @abstractmethod
    def get_query(self, dataset: str, q_id: str) -> Query:
        pass

    @abstractmethod
    def get_document(self, corpus: str, doc_id: str) -> Document:
        pass


class Searcher(ABC):
    @abstractmethod
    def search(self, query: str) -> SearchResult:
        pass


class Scorer(ABC):
    @abstractmethod
    def score(self, query: str, document: str, document_id: str) -> float:
        pass


class TestDataStore(DataStore):
    ds = {
        "beir/fiqa/test": ir_datasets.load("beir/fiqa/test"),
    }
    corpora = {
        "beir/fiqa": ir_datasets.load("beir/fiqa"),
    }

    def available_corpora(self) -> list[CorpusDescription]:
        return [
            CorpusDescription(name=name, num_documents=corpus.docs_count())
            for name, corpus in self.corpora.items()
        ]

    def available_datasets(self) -> list[DatasetDescription]:
        return [
            DatasetDescription(
                name=ds_name,
                corpus=ds_name.split("/")[0],
                num_queries=ds.queries_count(),
                num_qrels=ds.qrels_count(),
            )
            for ds_name, ds in self.ds.items()
        ]

    def list_queries(self, dataset: str, start_index: int, num: int) -> list[Query]:
        return [
            Query(id=x.query_id, text=x.text) for x in self.ds[dataset].queries_iter()
        ][start_index : start_index + num]

    def list_documents(self, corpus: str, start_index: int, num: int) -> list[Document]:
        return [
            Document(id=x.doc_id, text=x.text)
            for x in self.ds[corpus].docs_iter()[start_index : start_index + num]
        ]

    def get_query(self, dataset: str, q_id: str) -> Query:
        for query in self.ds[dataset].queries_iter():
            if query.query_id == q_id:
                return Query(id=query.query_id, text=query.text)
        raise HTTPException(404)

    def get_document(self, corpus: str, doc_id: str) -> Document:
        doc = self.ds[corpus].docs_store().get(doc_id)
        return Document(id=doc.doc_id, text=doc.text)
