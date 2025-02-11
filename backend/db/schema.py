from sqlalchemy import (
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    UniqueConstraint,
    func,
    literal_column,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

ORMBase = declarative_base()


class ORMCorpus(ORMBase):
    """ORM class representing a corpus."""

    __tablename__ = "corpora"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)

    datasets: Mapped[list["ORMDataset"]] = relationship(back_populates="corpus")


class ORMDataset(ORMBase):
    """ORM class representing a dataset."""

    __tablename__ = "datasets"
    __table_args__ = (UniqueConstraint("name", "corpus_id"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    corpus_id: Mapped[int] = mapped_column(ForeignKey("corpora.id"))

    corpus: Mapped[ORMCorpus] = relationship(back_populates="datasets")


class ORMQuery(ORMBase):
    """ORM class representing a query."""

    __tablename__ = "queries"

    id: Mapped[str] = mapped_column(primary_key=True)
    dataset_id: Mapped[int] = mapped_column(ForeignKey("datasets.id"), primary_key=True)
    text: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)

    dataset: Mapped["ORMDataset"] = relationship()
    qrels: Mapped[list["ORMQRel"]] = relationship(back_populates="query")


class ORMDocument(ORMBase):
    """ORM class representing a document."""

    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(primary_key=True)
    corpus_id: Mapped[int] = mapped_column(ForeignKey("corpora.id"), primary_key=True)
    title: Mapped[str] = mapped_column(nullable=True)
    text: Mapped[str] = mapped_column()

    corpus: Mapped["ORMCorpus"] = relationship()
    qrels: Mapped[list["ORMQRel"]] = relationship(back_populates="document")

    __table_args__ = (
        Index(
            "idx_tsv_text",
            func.to_tsvector(literal_column("'english'"), text.column),
            postgresql_using="gin",
        ),
    )


class ORMQRel(ORMBase):
    """ORM class representing a query relevance judgment (QRel)."""

    __tablename__ = "qrels"
    __table_args__ = (
        ForeignKeyConstraint(
            ["query_id", "dataset_id"],
            ["queries.id", "queries.dataset_id"],
        ),
        ForeignKeyConstraint(
            ["document_id", "corpus_id"],
            ["documents.id", "documents.corpus_id"],
        ),
    )

    query_id: Mapped[str] = mapped_column(primary_key=True)
    document_id: Mapped[str] = mapped_column(primary_key=True)
    dataset_id: Mapped[int] = mapped_column(primary_key=True)
    corpus_id: Mapped[int] = mapped_column(primary_key=True)
    relevance: Mapped[int]

    query: Mapped["ORMQuery"] = relationship(back_populates="qrels")
    document: Mapped["ORMDocument"] = relationship(back_populates="qrels")
