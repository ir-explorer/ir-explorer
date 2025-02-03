from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Column, ForeignKeyConstraint, Integer, Table


class Base(DeclarativeBase):
    pass


qrels_table = Table(
    "qrels",
    Base.metadata,
    Column("query_id"),
    Column("dataset"),
    Column("document_id"),
    Column("corpus"),
    ForeignKeyConstraint(["query_id", "dataset"], ["queries.id", "queries.dataset"]),
    ForeignKeyConstraint(
        ["document_id", "corpus"], ["documents.id", "documents.corpus"]
    ),
    Column("relevance", Integer()),
)


class Query(Base):
    __tablename__ = "queries"
    id: Mapped[str] = mapped_column(primary_key=True)
    dataset: Mapped[str] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)
    relevant_documents: Mapped[list["Document"]] = relationship(secondary=qrels_table)


class Document(Base):
    __tablename__ = "documents"
    id: Mapped[str] = mapped_column(primary_key=True)
    corpus: Mapped[str] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column()
    title: Mapped[str] = mapped_column(nullable=True)
