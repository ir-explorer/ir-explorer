from abc import ABC, abstractmethod

import ir_datasets
from pydantic import BaseModel


class CorpusInfo(BaseModel):
    name: str
    num_documents: int


class DatasetInfo(BaseModel):
    name: str
    corpus: str
    num_queries: int
    num_qrels: int


class SearchHit(BaseModel):
    document_id: str
    score: float


class SearchResult(BaseModel):
    query: str
    result: list[SearchHit]


class DataStore(ABC):
    @abstractmethod
    def available_corpora(self) -> list[CorpusInfo]:
        pass

    @abstractmethod
    def available_datasets(self) -> list[DatasetInfo]:
        pass

    @abstractmethod
    def list_queries(
        self, dataset: str, start_index: int, num: int
    ) -> list[dict[str, str]]:
        pass

    @abstractmethod
    def list_documents(
        self, dataset: str, start_index: int, num: int
    ) -> list[dict[str, str]]:
        pass

    @abstractmethod
    def get_query(self, dataset: str, q_id: str) -> dict[str, str]:
        pass

    @abstractmethod
    def get_document(self, dataset: str, doc_id: str) -> dict[str, str]:
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

    def available_corpora(self) -> list[CorpusInfo]:
        result = []
        for ds_name, ds in self.ds.items():
            result.append(
                {
                    "name": ds_name.split("/")[0],
                    "num_documents": ds.docs_count(),
                }
            )
        return result

    def available_datasets(self) -> list[DatasetInfo]:
        result = []
        for ds_name, ds in self.ds.items():
            result.append(
                {
                    "name": ds_name,
                    "corpus": ds_name.split("/")[0],
                    "num_queries": ds.queries_count(),
                    "num_qrels": ds.qrels_count(),
                }
            )
        return result

    def list_queries(
        self, dataset: str, start_index: int, num: int
    ) -> list[dict[str, str]]:
        return [x._asdict() for x in self.ds[dataset].queries_iter()][
            start_index : start_index + num
        ]

    def list_documents(
        self, dataset: str, start_index: int, num: int
    ) -> list[dict[str, str]]:
        return [
            x._asdict()
            for x in self.ds[dataset].docs_iter()[start_index : start_index + num]
        ]

    def get_query(self, dataset: str, q_id: str) -> dict[str, str]:
        for query in self.ds[dataset].queries_iter():
            if query.query_id == q_id:
                return query._asdict()
        return {}

    def get_document(self, dataset: str, doc_id: str) -> dict[str, str]:
        docstore = self.ds[dataset].docs_store()
        return docstore.get(doc_id)._asdict()
