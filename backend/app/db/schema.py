from sqlalchemy import (
    Column,
    Computed,
    ForeignKey,
    Index,
    Integer,
    UniqueConstraint,
    func,
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

    pkey: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(unique=True)
    language: Mapped[str] = mapped_column()

    datasets: Mapped[list["ORMDataset"]] = relationship(back_populates="corpus")

    __tablename__ = "corpora"


class ORMDataset(ORMBase):
    """ORM class representing a dataset."""

    pkey: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column()
    corpus_pkey: Mapped[int] = mapped_column(ForeignKey("corpora.pkey"))
    min_relevance: Mapped[int] = mapped_column()

    corpus: Mapped[ORMCorpus] = relationship(back_populates="datasets")

    __tablename__ = "datasets"
    __table_args__ = (UniqueConstraint("name", "corpus_pkey"),)


class ORMQuery(ORMBase):
    """ORM class representing a query."""

    pkey: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    id: Mapped[str] = mapped_column(index=True)
    dataset_pkey: Mapped[int] = mapped_column(ForeignKey("datasets.pkey"), index=True)
    text: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)

    dataset: Mapped["ORMDataset"] = relationship()
    qrels: Mapped[list["ORMQRel"]] = relationship(back_populates="query")

    __tablename__ = "queries"
    __table_args__ = (
        UniqueConstraint("id", "dataset_pkey"),
        Index(
            "ix_queries_search",
            pkey,
            text,
            description,
            dataset_pkey,
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


class ORMDocument(ORMBase):
    """ORM class representing a document."""

    pkey: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    id: Mapped[str] = mapped_column(index=True)
    corpus_pkey: Mapped[int] = mapped_column(ForeignKey("corpora.pkey"), index=True)
    title: Mapped[str] = mapped_column(nullable=True)
    text: Mapped[str] = mapped_column()

    text_length = Column(Integer, Computed(func.length(text)), index=True)

    corpus: Mapped["ORMCorpus"] = relationship()
    qrels: Mapped[list["ORMQRel"]] = relationship(back_populates="document")

    __tablename__ = "documents"
    __table_args__ = (
        Index(
            "ix_documents_search",
            pkey,
            title,
            text,
            corpus_pkey,
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
        Index("ix_documents_length", corpus_pkey, text_length),
    )


class ORMQRel(ORMBase):
    """ORM class representing a query relevance judgment (QRel)."""

    query_pkey: Mapped[str] = mapped_column(
        ForeignKey("queries.pkey"), primary_key=True, index=True
    )
    document_pkey: Mapped[str] = mapped_column(
        ForeignKey("documents.pkey"), primary_key=True, index=True
    )
    relevance: Mapped[int] = mapped_column()

    query: Mapped["ORMQuery"] = relationship(back_populates="qrels")
    document: Mapped["ORMDocument"] = relationship(back_populates="qrels")

    __tablename__ = "qrels"
