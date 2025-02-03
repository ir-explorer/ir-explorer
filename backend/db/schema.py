from sqlalchemy import (
    ForeignKeyConstraint,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class ORMBase(DeclarativeBase):
    pass


class ORMQRel(ORMBase):
    __tablename__ = "qrels"
    __table_args__ = (
        ForeignKeyConstraint(
            ["query_id", "dataset"],
            ["queries.id", "queries.dataset"],
        ),
        ForeignKeyConstraint(
            ["document_id", "corpus"], ["documents.id", "documents.corpus"]
        ),
    )

    query_id: Mapped[str] = mapped_column(primary_key=True)
    dataset: Mapped[str] = mapped_column(primary_key=True)
    query: Mapped["ORMQuery"] = relationship(
        foreign_keys=[query_id, dataset], back_populates="qrels"
    )

    document_id: Mapped[str] = mapped_column(primary_key=True)
    corpus: Mapped[str] = mapped_column(primary_key=True)
    document: Mapped["ORMDocument"] = relationship(
        foreign_keys=[document_id, corpus], back_populates="qrels"
    )

    relevance: Mapped[int]


class ORMQuery(ORMBase):
    __tablename__ = "queries"

    id: Mapped[str] = mapped_column(primary_key=True)
    dataset: Mapped[str] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)

    qrels: Mapped[list[ORMQRel]] = relationship(back_populates="query")


class ORMDocument(ORMBase):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(primary_key=True)
    corpus: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=True)
    text: Mapped[str] = mapped_column()

    qrels: Mapped[list[ORMQRel]] = relationship(back_populates="document")
