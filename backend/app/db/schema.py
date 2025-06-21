from sqlalchemy import (
    ForeignKey,
    Index,
    UniqueConstraint,
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
    pkey: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(unique=True)
    language: Mapped[str] = mapped_column()

    datasets: Mapped[list["ORMDataset"]] = relationship(back_populates="corpus")


class ORMDataset(ORMBase):
    """ORM class representing a dataset."""

    __tablename__ = "datasets"
    __table_args__ = (UniqueConstraint("name", "corpus_pkey"),)
    pkey: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column()
    corpus_pkey: Mapped[int] = mapped_column(ForeignKey("corpora.pkey"))
    min_relevance: Mapped[int] = mapped_column()

    corpus: Mapped[ORMCorpus] = relationship(back_populates="datasets")


class ORMQuery(ORMBase):
    """ORM class representing a query."""

    __tablename__ = "queries"
    __table_args__ = (UniqueConstraint("id", "dataset_pkey"),)
    pkey: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    id: Mapped[str] = mapped_column(index=True)
    dataset_pkey: Mapped[int] = mapped_column(ForeignKey("datasets.pkey"), index=True)
    text: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)

    dataset: Mapped["ORMDataset"] = relationship()
    qrels: Mapped[list["ORMQRel"]] = relationship(back_populates="query")


class ORMDocument(ORMBase):
    """ORM class representing a document."""

    __tablename__ = "documents"
    __table_args__ = (
        Index(
            None,
            "pkey",
            "title",
            "text",
            "corpus_pkey",
            postgresql_using="bm25",
            postgresql_with={
                "key_field": "pkey",
                "text_fields": """\'{
                    "text": {
                        "tokenizer": {
                            "type": "default",
                            "stemmer": "English",
                            "stopwords_language": "English"
                        }
                    }
                }\'""",
            },
        ),
    )
    pkey: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    id: Mapped[str] = mapped_column(index=True)
    corpus_pkey: Mapped[int] = mapped_column(ForeignKey("corpora.pkey"), index=True)
    title: Mapped[str] = mapped_column(nullable=True)
    text: Mapped[str] = mapped_column()

    corpus: Mapped["ORMCorpus"] = relationship()
    qrels: Mapped[list["ORMQRel"]] = relationship(back_populates="document")


class ORMQRel(ORMBase):
    """ORM class representing a query relevance judgment (QRel)."""

    __tablename__ = "qrels"

    query_pkey: Mapped[str] = mapped_column(
        ForeignKey("queries.pkey"), primary_key=True, index=True
    )
    document_pkey: Mapped[str] = mapped_column(
        ForeignKey("documents.pkey"), primary_key=True, index=True
    )
    relevance: Mapped[int] = mapped_column()

    query: Mapped["ORMQuery"] = relationship(back_populates="qrels")
    document: Mapped["ORMDocument"] = relationship(back_populates="qrels")
