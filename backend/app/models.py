from dataclasses import dataclass


@dataclass
class Corpus:
    """A corpus."""

    name: str
    language: str


@dataclass
class Dataset:
    """A dataset."""

    name: str
    corpus_name: str
    min_relevance: int = 1


@dataclass
class BulkQRel:
    """A single query-document relevance score for bulk insertion."""

    query_id: str
    document_id: str
    relevance: int


@dataclass
class QRel(BulkQRel):
    """A single query-document relevance score."""

    corpus_name: str
    dataset_name: str


@dataclass
class BulkQuery:
    """A single query for bulk insertion."""

    id: str
    text: str
    description: str | None


@dataclass
class Query(BulkQuery):
    """A single query."""

    corpus_name: str
    dataset_name: str


@dataclass
class QueryWithRelevanceInfo(Query):
    """A single query with relevance information attached."""

    num_relevant_documents: int


@dataclass
class BulkDocument:
    """A single document for bulk insertion."""

    id: str
    title: str | None
    text: str


@dataclass
class Document(BulkDocument):
    """A single document."""

    corpus_name: str


@dataclass
class DocumentWithRelevance(Document):
    """A single document with a relevance (w.r.t. a specific query)."""

    query_id: str
    relevance: int


@dataclass
class DocumentSearchHit:
    """A document retrieved by a search engine."""

    id: str
    title: str | None
    snippet: str
    score: float
    corpus_name: str


@dataclass
class DocumentSearchResult:
    """An incomplete list of retrieved documents."""

    total_num_items: int
    offset: int
    items: list[DocumentSearchHit]
