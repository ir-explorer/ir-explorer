from typing import TYPE_CHECKING

from db import provide_transaction
from db.schema import ORMCorpus, ORMDataset, ORMDocument, ORMQRel, ORMQuery
from litestar import Controller, delete, post
from litestar.di import Provide
from litestar.exceptions import HTTPException
from litestar.status_codes import (
    HTTP_400_BAD_REQUEST,
    HTTP_409_CONFLICT,
)

# litestar needs these outside of the type checking block
from models import (
    CorpusInfo,  # noqa: TC002
    DatasetInfo,  # noqa: TC002
    DocumentInfo,  # noqa: TC002
    QRelInfo,  # noqa: TC002
    QueryInfo,  # noqa: TC002
)
from sqlalchemy import (
    and_,
    insert,
    select,
)
from sqlalchemy import delete as delete_
from sqlalchemy.exc import IntegrityError, ProgrammingError
from sqlalchemy.orm import joinedload

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.ext.asyncio import AsyncSession


class DataController(Controller):
    """Controller that handles data-related API endpoints."""

    dependencies = {"db_transaction": Provide(provide_transaction)}

    @post(path="/create_corpus")
    async def create_corpus(
        self, db_transaction: "AsyncSession", data: "CorpusInfo"
    ) -> None:
        """Create a new corpus in the database.

        :param db_transaction: A DB transaction.
        :param data: The corpus.
        :raises HTTPException: When the corpus cannot be added to the database.
        """
        # for now, only english is supported
        if data.language != "English":
            raise HTTPException(
                "Unsupported language.",
                status_code=HTTP_400_BAD_REQUEST,
                extra={"language": data.language},
            )

        sql = insert(ORMCorpus).values({"name": data.name, "language": data.language})

        try:
            await db_transaction.execute(sql)
        except (IntegrityError, ProgrammingError) as e:
            raise HTTPException(
                "Failed to add corpus.",
                status_code=HTTP_409_CONFLICT,
                extra={"corpus_name": data.name, "error_code": e.code},
            )

    @post(path="/create_dataset")
    async def create_dataset(
        self, db_transaction: "AsyncSession", data: "DatasetInfo"
    ) -> None:
        """Create a new dataset in the database.

        :param db_transaction: A DB transaction.
        :param data: The dataset.
        :raises HTTPException: When the dataset cannot be added to the database.
        """
        sql = insert(ORMDataset).values(
            {
                "name": data.name,
                "corpus_pkey": select(ORMCorpus.pkey)
                .filter_by(name=data.corpus_name)
                .scalar_subquery(),
                "min_relevance": data.min_relevance,
            }
        )

        try:
            await db_transaction.execute(sql)
        except IntegrityError as e:
            raise HTTPException(
                "Failed to add dataset.",
                status_code=HTTP_409_CONFLICT,
                extra={
                    "name": data.name,
                    "corpus_name": data.corpus_name,
                    "error_code": e.code,
                },
            )

    @post(path="/add_queries")
    async def add_queries(
        self,
        db_transaction: "AsyncSession",
        dataset_name: str,
        corpus_name: str,
        data: "Sequence[QueryInfo]",
    ) -> None:
        """Insert new queries into the database.

        :param db_transaction: A DB transaction.
        :param dataset_name: The dataset the queries belong to.
        :param corpus_name: The corpus the dataset belongs to.
        :param data: The queries to insert.
        :raises HTTPException: When the queries cannot be added to the database.
        """
        dataset_cte = (
            select(ORMDataset)
            .join(ORMCorpus)
            .where(
                and_(
                    ORMDataset.name == dataset_name,
                    ORMCorpus.name == corpus_name,
                )
            )
        ).cte()
        sql = insert(ORMQuery).values(
            [
                {
                    "id": q.id,
                    "dataset_pkey": select(dataset_cte.c.pkey),
                    "text": q.text,
                    "description": q.description,
                }
                for q in data
            ]
        )

        try:
            await db_transaction.execute(sql)
        except IntegrityError as e:
            raise HTTPException(
                "Failed to add queries.",
                status_code=HTTP_409_CONFLICT,
                extra={"error_code": e.code},
            )

    @post(path="/add_documents")
    async def add_documents(
        self,
        db_transaction: "AsyncSession",
        corpus_name: str,
        data: "Sequence[DocumentInfo]",
    ) -> None:
        """Insert new documents into the database.

        :param db_transaction: A DB transaction.
        :param corpus_name: The corpus the documents belong to.
        :param data: The documents to insert.
        :raises HTTPException: When the documents cannot be added to the database.
        """
        corpus_cte = select(ORMCorpus).where(ORMCorpus.name == corpus_name).cte()
        sql = insert(ORMDocument).values(
            [
                {
                    "id": doc.id,
                    "corpus_pkey": select(corpus_cte.c.pkey),
                    "title": doc.title,
                    "text": doc.text,
                }
                for doc in data
            ]
        )

        try:
            await db_transaction.execute(sql)
        except IntegrityError as e:
            raise HTTPException(
                "Failed to add Documents.",
                status_code=HTTP_409_CONFLICT,
                extra={"error_code": e.code},
            )

    @post(path="/add_qrels")
    async def add_qrels(
        self,
        db_transaction: "AsyncSession",
        dataset_name: str,
        corpus_name: str,
        data: "Sequence[QRelInfo]",
    ) -> None:
        """Insert QRels into the database.

        :param db_transaction: A DB transaction.
        :param dataset_name: The dataset the QRels belong to.
        :param corpus_name: The corpus the dataset belongs to.
        :param data: The QRels to insert.
        :raises HTTPException: When the QRels cannot be added to the database.
        """
        dataset_cte = (
            select(ORMDataset)
            .join(ORMCorpus)
            .where(
                and_(
                    ORMDataset.name == dataset_name,
                    ORMCorpus.name == corpus_name,
                )
            )
        ).cte()
        sql = insert(ORMQRel).values(
            [
                {
                    "query_pkey": select(ORMQuery.pkey)
                    .where(
                        ORMQuery.id == qrel.query_id,
                        ORMQuery.dataset_pkey == dataset_cte.c.pkey,
                    )
                    .scalar_subquery(),
                    "document_pkey": select(ORMDocument.pkey)
                    .where(
                        ORMDocument.id == qrel.document_id,
                        ORMDocument.corpus_pkey == dataset_cte.c.corpus_pkey,
                    )
                    .scalar_subquery(),
                    "relevance": qrel.relevance,
                }
                for qrel in data
            ]
        )

        try:
            await db_transaction.execute(sql)
        except IntegrityError as e:
            raise HTTPException(
                "Failed to add QRels.",
                status_code=HTTP_409_CONFLICT,
                extra={"error_code": e.code},
            )

    @delete(path="/remove_dataset")
    async def remove_dataset(
        self, db_transaction: "AsyncSession", corpus_name: str, dataset_name: str
    ) -> None:
        """Remove a dataset and its associated queries and QRels.

        :param db_transaction: A DB transaction.
        :param corpus_name: The name of the corpus the dataset is in.
        :param dataset_name: The name of the dataset to remove.
        """
        dataset_pkey = (
            select(ORMDataset.pkey)
            .join(ORMCorpus)
            .where(and_(ORMDataset.name == dataset_name, ORMCorpus.name == corpus_name))
        ).scalar_subquery()
        sql_del_qrels = delete_(ORMQRel).where(
            ORMQRel.query_pkey == ORMQuery.pkey, ORMQuery.dataset_pkey == dataset_pkey
        )
        sql_del_queries = delete_(ORMQuery).filter_by(dataset_pkey=dataset_pkey)
        sql_del_dataset = delete_(ORMDataset).filter_by(pkey=dataset_pkey)

        await db_transaction.execute(sql_del_qrels)
        await db_transaction.execute(sql_del_queries)
        await db_transaction.execute(sql_del_dataset)

    @delete(path="/remove_corpus")
    async def remove_corpus(
        self, db_transaction: "AsyncSession", corpus_name: str
    ) -> None:
        """Remove a corpus and its associated documents.

        Any associated datasets must be removed first.

        :param db_transaction: A DB transaction.
        :param corpus_name: The name of the corpus to remove.
        :raises HTTPException: When the corpus still has associated datasets.
        :raises HTTPException: When the corpus cannot be removed for other reasons.
        """
        sql_corpus = (
            select(ORMCorpus)
            .options(joinedload(ORMCorpus.datasets))
            .filter_by(name=corpus_name)
        )
        corpus = (await db_transaction.execute(sql_corpus)).unique().scalar_one()
        if len(corpus.datasets) > 0:
            raise HTTPException(
                "Associated datasets must be removed first.",
                status_code=HTTP_409_CONFLICT,
                extra={"corpus_name": corpus_name},
            )

        sql_del_documents = delete_(ORMDocument).filter_by(corpus_pkey=corpus.pkey)
        sql_del_corpus = delete_(ORMCorpus).filter_by(name=corpus_name)

        try:
            await db_transaction.execute(sql_del_documents)
            await db_transaction.execute(sql_del_corpus)
        except IntegrityError as e:
            raise HTTPException(
                "Failed to remove corpus.",
                status_code=HTTP_409_CONFLICT,
                extra={"corpus_name": corpus_name, "error_code": e.code},
            )
