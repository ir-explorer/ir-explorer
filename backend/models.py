from dataclasses import dataclass


@dataclass
class Dataset:
    """A dataset."""

    name: str
    corpus_name: str


@dataclass
class QRel:
    """A single query-document relevance score."""

    query_id: str
    document_id: str
    corpus_name: str
    dataset_name: str
    relevance: int


@dataclass
class Query:
    """A single query."""

    id: str
    corpus_name: str
    dataset_name: str
    text: str
    description: str | None


@dataclass
class QueryWithRelevanceInfo(Query):
    """A single query with relevance information attached."""

    num_relevant_documents: int


@dataclass
class Document:
    """A single document."""

    id: str
    corpus_name: str
    title: str | None
    text: str


@dataclass
class DocumentWithRelevance(Document):
    """A single document with a relevance (w.r.t. a specific query)."""

    query_id: str
    relevance: int
