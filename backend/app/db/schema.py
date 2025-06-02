from sqlalchemy import (
    DDL,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    UniqueConstraint,
    event,
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

    name: Mapped[str]
    corpus_pkey: Mapped[int] = mapped_column(ForeignKey("corpora.pkey"))
    min_relevance: Mapped[int] = mapped_column()

    corpus: Mapped[ORMCorpus] = relationship(back_populates="datasets")


class ORMQuery(ORMBase):
    """ORM class representing a query."""

    __tablename__ = "queries"
    __table_args__ = (UniqueConstraint("id", "dataset_pkey"),)
    pkey: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    id: Mapped[str] = mapped_column()
    dataset_pkey: Mapped[int] = mapped_column(ForeignKey("datasets.pkey"))
    text: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)

    dataset: Mapped["ORMDataset"] = relationship()
    qrels: Mapped[list["ORMQRel"]] = relationship(back_populates="query")


class ORMDocument(ORMBase):
    """ORM class representing a document."""

    __tablename__ = "documents"
    __table_args__ = (
        UniqueConstraint("id", "corpus_pkey"),
        # index of foreign key to speed up deletion
        Index(None, "corpus_pkey"),
    )
    pkey: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    id: Mapped[str] = mapped_column()
    corpus_pkey: Mapped[int] = mapped_column(ForeignKey("corpora.pkey"))
    title: Mapped[str] = mapped_column(nullable=True)
    text: Mapped[str] = mapped_column()

    corpus: Mapped["ORMCorpus"] = relationship()
    qrels: Mapped[list["ORMQRel"]] = relationship(back_populates="document")


class ORMQRel(ORMBase):
    """ORM class representing a query relevance judgment (QRel)."""

    __tablename__ = "qrels"
    __table_args__ = (
        # indexes of foreign keys to speed up deletion
        Index(None, "query_pkey"),
        Index(None, "document_pkey"),
    )

    query_pkey: Mapped[str] = mapped_column(
        ForeignKey("queries.pkey"), primary_key=True
    )
    document_pkey: Mapped[str] = mapped_column(
        ForeignKey("documents.pkey"), primary_key=True
    )
    relevance: Mapped[int] = mapped_column()

    query: Mapped["ORMQuery"] = relationship(back_populates="qrels")
    document: Mapped["ORMDocument"] = relationship(back_populates="qrels")


# functions to estimate the number of documents and queries
# https://wiki.postgresql.org/wiki/Count_estimate

event.listen(
    ORMBase.metadata,
    "after_create",
    DDL(
        """
        CREATE OR REPLACE
        FUNCTION estimate_num_docs(corpus_pkey int)
        RETURNS int
        LANGUAGE plpgsql
        AS
        $function$
        DECLARE
            plan jsonb;
        BEGIN
            EXECUTE FORMAT(
                'EXPLAIN (FORMAT JSON) SELECT * FROM documents WHERE corpus_pkey = %%s',
                corpus_pkey
            ) INTO plan;
            RETURN plan->0->'Plan'->'Plan Rows';
        END;
        $function$;
        """
    ),
)

event.listen(
    ORMBase.metadata,
    "after_create",
    DDL(
        """
        CREATE OR REPLACE
        FUNCTION estimate_num_queries(dataset_pkey int)
        RETURNS int
        LANGUAGE plpgsql
        AS
        $function$
        DECLARE
            plan jsonb;
        BEGIN
            EXECUTE FORMAT(
                'EXPLAIN (FORMAT JSON) SELECT * FROM queries WHERE dataset_pkey = %%s',
                dataset_pkey
            ) INTO plan;
            RETURN plan->0->'Plan'->'Plan Rows';
        END;
        $function$;
        """
    ),
)
