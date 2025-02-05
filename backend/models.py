from dataclasses import dataclass


@dataclass
class Document:
    """A single document."""

    id: str
    corpus: str
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
    dataset: str
    text: str
    description: str | None
    num_relevant_documents: int


@dataclass
class QRel:
    """A single query-document relevance score."""

    query_id: str
    dataset: str
    document_id: str
    corpus: str
    relevance: int
