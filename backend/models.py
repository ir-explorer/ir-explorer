from dataclasses import dataclass


@dataclass
class Document:
    id: str
    corpus: str
    title: str | None
    text: str


@dataclass
class RelevantDocument(Document):
    relevance: int


@dataclass
class Query:
    id: str
    dataset: str
    text: str
    description: str | None
    num_relevant_documents: int


@dataclass
class QRel:
    query_id: str
    dataset: str
    document_id: str
    corpus: str
    relevance: int
