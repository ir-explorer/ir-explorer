from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class ORMBase(DeclarativeBase):
    """Declarative base for ORM schema."""

    pass


class ORMCorpus(ORMBase):
    """ORM class representing a corpus."""

    __tablename__ = "corpora"

    name: Mapped[str] = mapped_column(primary_key=True)

    datasets: Mapped[list["ORMDataset"]] = relationship(back_populates="corpus")


class ORMDataset(ORMBase):
    """ORM class representing a dataset."""

    __tablename__ = "datasets"

    name: Mapped[str] = mapped_column(primary_key=True)
    corpus_name: Mapped[str] = mapped_column(ForeignKey("corpora.name"))

    corpus: Mapped[ORMCorpus] = relationship(back_populates="datasets")


class ORMQuery(ORMBase):
    """ORM class representing a query."""

    __tablename__ = "queries"

    id: Mapped[str] = mapped_column(primary_key=True)
    dataset_name: Mapped[str] = mapped_column(
        ForeignKey("datasets.name"), primary_key=True
    )
    text: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)

    dataset: Mapped["ORMDataset"] = relationship()
    qrels: Mapped[list["ORMQRel"]] = relationship(back_populates="query")


class ORMDocument(ORMBase):
    """ORM class representing a document."""

    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(primary_key=True)
    corpus_name: Mapped[str] = mapped_column(
        ForeignKey("corpora.name"), primary_key=True
    )
    title: Mapped[str] = mapped_column(nullable=True)
    text: Mapped[str] = mapped_column()

    corpus: Mapped["ORMCorpus"] = relationship()
    qrels: Mapped[list["ORMQRel"]] = relationship(back_populates="document")


class ORMQRel(ORMBase):
    """ORM class representing a query relevance judgment (QRel)."""

    __tablename__ = "qrels"
    __table_args__ = (
        ForeignKeyConstraint(
            ["query_id", "dataset_name"],
            ["queries.id", "queries.dataset_name"],
        ),
        ForeignKeyConstraint(
            ["document_id", "corpus_name"],
            ["documents.id", "documents.corpus_name"],
        ),
    )

    query_id: Mapped[str] = mapped_column(primary_key=True)
    dataset_name: Mapped[str] = mapped_column(primary_key=True)
    document_id: Mapped[str] = mapped_column(primary_key=True)
    corpus_name: Mapped[str] = mapped_column(primary_key=True)
    relevance: Mapped[int]

    query: Mapped["ORMQuery"] = relationship(back_populates="qrels")
    document: Mapped["ORMDocument"] = relationship(back_populates="qrels")
