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

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    language: Mapped[str] = mapped_column()

    datasets: Mapped[list["ORMDataset"]] = relationship(back_populates="corpus")


class ORMDataset(ORMBase):
    """ORM class representing a dataset."""

    __tablename__ = "datasets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    corpus_id: Mapped[int] = mapped_column(ForeignKey("corpora.id"))
    min_relevance: Mapped[int]

    corpus: Mapped[ORMCorpus] = relationship(back_populates="datasets")

    __table_args__ = (UniqueConstraint("name", "corpus_id"),)


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
        # index of foreign key to speed up deletion
        Index(None, corpus_id),
    )


class ORMQRel(ORMBase):
    """ORM class representing a query relevance judgment (QRel)."""

    __tablename__ = "qrels"

    query_id: Mapped[str] = mapped_column(primary_key=True)
    document_id: Mapped[str] = mapped_column(primary_key=True)
    dataset_id: Mapped[int] = mapped_column(primary_key=True)
    corpus_id: Mapped[int] = mapped_column(primary_key=True)
    relevance: Mapped[int]

    query: Mapped["ORMQuery"] = relationship(back_populates="qrels")
    document: Mapped["ORMDocument"] = relationship(back_populates="qrels")

    __table_args__ = (
        ForeignKeyConstraint(
            ["query_id", "dataset_id"],
            ["queries.id", "queries.dataset_id"],
        ),
        ForeignKeyConstraint(
            ["document_id", "corpus_id"],
            ["documents.id", "documents.corpus_id"],
        ),
        # indexes of foreign keys to speed up deletion
        Index(None, document_id),
        Index(None, dataset_id),
        Index(None, corpus_id),
    )


# functions to estimate the number of documents and queries
# https://wiki.postgresql.org/wiki/Count_estimate

event.listen(
    ORMBase.metadata,
    "after_create",
    DDL(
        """
        CREATE OR REPLACE
        FUNCTION estimate_num_docs(corpus_id int)
        RETURNS int
        LANGUAGE plpgsql
        AS
        $function$
        DECLARE
            plan jsonb;
        BEGIN
            EXECUTE FORMAT(
                'EXPLAIN (FORMAT JSON) SELECT * FROM documents WHERE corpus_id = %%s',
                corpus_id
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
        FUNCTION estimate_num_queries(dataset_id int)
        RETURNS int
        LANGUAGE plpgsql
        AS
        $function$
        DECLARE
            plan jsonb;
        BEGIN
            EXECUTE FORMAT(
                'EXPLAIN (FORMAT JSON) SELECT * FROM queries WHERE dataset_id = %%s',
                dataset_id
            ) INTO plan;
            RETURN plan->0->'Plan'->'Plan Rows';
        END;
        $function$;
        """
    ),
)
