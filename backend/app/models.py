from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class CorpusInfo:
    """A corpus for insertion."""

    name: str
    language: str


@dataclass
class Corpus(CorpusInfo):
    """A corpus with statistics."""

    num_datasets: int
    num_documents_estimate: int


@dataclass
class DatasetInfo:
    """A dataset for insertion."""

    name: str
    corpus_name: str
    min_relevance: int = 1


@dataclass
class Dataset:
    """A dataset with statistics."""

    name: str
    corpus_name: str
    min_relevance: int
    num_queries_estimate: int


@dataclass
class QRelInfo:
    """A single query-document relevance score for bulk insertion."""

    query_id: str
    document_id: str
    relevance: int


@dataclass
class QRel(QRelInfo):
    """A single query-document relevance score."""

    corpus_name: str
    dataset_name: str


@dataclass
class QueryInfo:
    """A single query for bulk insertion."""

    id: str
    text: str
    description: str | None


@dataclass
class Query(QueryInfo):
    """A single query with statistics."""

    corpus_name: str
    dataset_name: str
    num_relevant_documents: int


@dataclass
class DocumentInfo:
    """A single document for bulk insertion."""

    id: str
    title: str | None
    text: str


@dataclass
class Document(DocumentInfo):
    """A single document."""

    corpus_name: str
    num_relevant_queries: int


@dataclass
class DocumentSearchHit:
    """A document retrieved by a search engine."""

    id: str
    title: str | None
    snippet: str
    score: float
    corpus_name: str


@dataclass
class Paginated(Generic[T]):
    """An incomplete list of items."""

    items: list[T]
    offset: int
    total_num_items: int
