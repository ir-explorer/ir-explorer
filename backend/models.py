from dataclasses import dataclass


@dataclass
class Document:
    """A single document."""

    id: str
    corpus_name: str
    title: str | None
    text: str


@dataclass
class RelevantDocument(Document):
    """A single document with a relevance (w.r.t. a specific query)."""

    relevance: int


@dataclass
class Query:
    """A single query."""

    id: str
    dataset_name: str
    text: str
    description: str | None
    num_relevant_documents: int


@dataclass
class QRel:
    """A single query-document relevance score."""

    query_id: str
    dataset_name: str
    document_id: str
    corpus_name: str
    relevance: int
