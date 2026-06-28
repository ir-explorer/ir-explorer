from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class AvailableOptions:
    """All available options."""

    query_languages: list[str]
    corpus_names: list[str]
    model_names: list[str]


@dataclass
class CorpusInfo:
    """Corpus attributes."""

    name: str
    language: str


@dataclass
class Corpus(CorpusInfo):
    """Corpus with attributes and statistics."""

    num_datasets: int
    num_documents: int


@dataclass
class DatasetInfo:
    """Dataset attributes."""

    name: str
    corpus_name: str
    relevance_threshold: int


@dataclass
class DatasetRelevanceInfo(DatasetInfo):
    """Dataset attributes including its relevance range."""

    min_relevance: int
    max_relevance: int


@dataclass
class Dataset(DatasetRelevanceInfo):
    """Dataset with attributes and statistics."""

    num_queries: int


@dataclass
class QueryInfo:
    """Query attributes."""

    id: str
    text: str
    description: str | None


@dataclass
class Query(QueryInfo):
    """Query with attributes, associated dataset, and statistics."""

    corpus_name: str
    dataset_name: str
    num_relevant_documents: int


@dataclass
class DocumentInfo:
    """Document attributes."""

    id: str
    title: str | None
    text: str


@dataclass
class Document(DocumentInfo):
    """Document with attributes, associated corpus, and statistics."""

    corpus_name: str
    num_relevant_queries: int


@dataclass
class DocumentSearchHit:
    """Document retrieved by a search engine."""

    id: str
    snippet: str
    score: float
    corpus_name: str


@dataclass
class QRelInfo:
    """QRel with IDs and relevance only."""

    query_id: str
    document_id: str
    relevance: int


@dataclass
class QRel:
    """QRel with attributes and relevance."""

    query_info: QueryInfo
    document_info: DocumentInfo
    dataset_relevance_info: DatasetRelevanceInfo
    relevance: int


@dataclass
class Paginated(Generic[T]):
    """Part of a list of items for pagination."""

    items: list[T]
    offset: int
    total_num_items: int
