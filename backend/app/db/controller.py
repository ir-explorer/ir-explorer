from typing import TYPE_CHECKING

from litestar import Controller, delete, get, post
from litestar.di import Provide
from litestar.exceptions import HTTPException
from litestar.status_codes import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)
from models import (
    Corpus,
    CorpusInfo,
    Dataset,
    DatasetInfo,
    Document,
    DocumentInfo,
    DocumentSearchHit,
    Paginated,
    QRel,
    QRelInfo,
    Query,
    QueryInfo,
    SearchOptions,
)
from sqlalchemy import (
    VARCHAR,
    SQLColumnExpression,
    and_,
    desc,
    func,
    insert,
    literal_column,
    select,
    text,
)
from sqlalchemy import delete as delete_
from sqlalchemy.exc import IntegrityError, NoResultFound, ProgrammingError
from sqlalchemy.orm import joinedload

from db import provide_transaction
from db.schema import ORMCorpus, ORMDataset, ORMDocument, ORMQRel, ORMQuery

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.ext.asyncio import AsyncSession


class DBController(Controller):
    """Controller that handles database related API endpoints."""

    dependencies = {"transaction": Provide(provide_transaction)}

    @get(path="/get_available_languages")
    def get_available_languages(self) -> list[str]:
        """List all corpus languages supported by the DB engine (for full-text search).

        :return: All available languages.
        """
        # currently, paradedb does not support configuration based on a language column,
        # so, for now, only english is supported
        # https://github.com/paradedb/paradedb/issues/1793
        return ["English"]

    @get(path="/get_search_options")
    async def get_search_options(self, transaction: "AsyncSession") -> SearchOptions:
        """Get available options for all search settings.

        :param transaction: A DB transaction.
        :return: The available options.
        """
        sql = select(ORMCorpus.name)
        result = (await transaction.execute(sql)).scalars()
        return SearchOptions(query_languages=["English"], corpus_names=list(result))

    @post(path="/create_corpus")
    async def create_corpus(
        self, transaction: "AsyncSession", data: CorpusInfo
    ) -> None:
        """Create a new corpus in the database.

        :param transaction: A DB transaction.
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
            await transaction.execute(sql)
        except (IntegrityError, ProgrammingError) as e:
            raise HTTPException(
                "Failed to add corpus.",
                status_code=HTTP_409_CONFLICT,
                extra={"corpus_name": data.name, "error_code": e.code},
            )

    @post(path="/create_dataset")
    async def create_dataset(
        self, transaction: "AsyncSession", data: DatasetInfo
    ) -> None:
        """Create a new dataset in the database.

        :param transaction: A DB transaction.
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
            await transaction.execute(sql)
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
        transaction: "AsyncSession",
        dataset_name: str,
        corpus_name: str,
        data: "Sequence[QueryInfo]",
    ) -> None:
        """Insert new queries into the database.

        :param transaction: A DB transaction.
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
            await transaction.execute(sql)
        except IntegrityError as e:
            raise HTTPException(
                "Failed to add queries.",
                status_code=HTTP_409_CONFLICT,
                extra={"error_code": e.code},
            )

    @post(path="/add_documents")
    async def add_documents(
        self,
        transaction: "AsyncSession",
        corpus_name: str,
        data: "Sequence[DocumentInfo]",
    ) -> None:
        """Insert new documents into the database.

        :param transaction: A DB transaction.
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
            await transaction.execute(sql)
        except IntegrityError as e:
            raise HTTPException(
                "Failed to add Documents.",
                status_code=HTTP_409_CONFLICT,
                extra={"error_code": e.code},
            )

    @post(path="/add_qrels")
    async def add_qrels(
        self,
        transaction: "AsyncSession",
        dataset_name: str,
        corpus_name: str,
        data: "Sequence[QRelInfo]",
    ) -> None:
        """Insert QRels into the database.

        :param transaction: A DB transaction.
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
            await transaction.execute(sql)
        except IntegrityError as e:
            raise HTTPException(
                "Failed to add QRels.",
                status_code=HTTP_409_CONFLICT,
                extra={"error_code": e.code},
            )

    @get(path="/get_corpora")
    async def get_corpora(self, transaction: "AsyncSession") -> list[Corpus]:
        """List all corpora including statistics about datasets and documents.

        :param transaction: A DB transaction.
        :return: The list of corpora.
        """
        sq_documents = (
            select(ORMDocument.corpus_pkey, func.count().label("count"))
            .group_by(ORMDocument.corpus_pkey)
            .subquery()
        )
        sq_datasets = (
            select(ORMDataset.corpus_pkey, func.count().label("count"))
            .group_by(ORMDataset.corpus_pkey)
            .subquery()
        )

        sql = (
            select(ORMCorpus, sq_documents.c.count, sq_datasets.c.count)
            .join(sq_documents)
            .join(sq_datasets)
        )

        result = (await transaction.execute(sql)).all()
        return [
            Corpus(
                name=corpus.name,
                language=corpus.language,
                num_datasets=num_datasets,
                num_documents=num_documents,
            )
            for corpus, num_documents, num_datasets in result
        ]

    @get(path="/get_datasets")
    async def get_datasets(
        self, transaction: "AsyncSession", corpus_name: str
    ) -> list[Dataset]:
        """List all datasets for a corpus, including statistics.

        :param transaction: A DB transaction.
        :param corpus_name: The name of the corpus.
        :return: The list of datasets.
        """
        sq_queries = (
            select(ORMQuery.dataset_pkey, func.count().label("count"))
            .group_by(ORMQuery.dataset_pkey)
            .subquery()
        )

        sql = (
            select(ORMDataset, sq_queries.c.count)
            .join(sq_queries)
            .join(ORMCorpus)
            .where(ORMCorpus.name == corpus_name)
        )

        result = (await transaction.execute(sql)).all()
        return [
            Dataset(
                name=dataset.name,
                corpus_name=corpus_name,
                min_relevance=dataset.min_relevance,
                num_queries=num_queries,
            )
            for dataset, num_queries in result
        ]

    @get(path="/get_queries")
    async def get_queries(
        self,
        transaction: "AsyncSession",
        corpus_name: str,
        dataset_name: str | None = None,
        match: str | None = None,
        num_results: int = 10,
        offset: int = 0,
    ) -> Paginated[Query]:
        """List queries.

        :param transaction: A DB transaction.
        :param corpus_name: The name of the corpus.
        :param dataset_name: Return only queries in this dataset.
        :param match: Return only queries matching this.
        :param num_results: How many queries to return.
        :param offset: Offset for pagination.
        :return: Paginated list of queries.
        """
        where_clauses = [ORMCorpus.name == corpus_name]
        if dataset_name is not None:
            where_clauses.append(ORMDataset.name == dataset_name)
        if match is not None:
            where_clauses.append(
                ORMQuery.pkey.bool_op("@@@")(
                    func.paradedb.fuzzy_term(literal_column("'text'"), match)
                )
            )

        sql_count = (
            select(func.count())
            .select_from(ORMQuery)
            .join(ORMDataset)
            .join(ORMCorpus)
            .where(*where_clauses)
        )

        sql = (
            select(
                ORMQuery.id,
                ORMQuery.text,
                ORMQuery.description,
                func.count().label("count"),
                ORMDataset.name,
            )
            .select_from(ORMQRel)
            .join(ORMQuery)
            .join(ORMDocument)
            .join(ORMDataset)
            .join(ORMCorpus)
            .where(*where_clauses, ORMQRel.relevance >= ORMDataset.min_relevance)
            .group_by(
                ORMQuery.pkey,
                ORMQuery.id,
                ORMQuery.description,
                ORMQuery.text,
                ORMDataset.name,
            )
            .order_by(desc(text("count")), ORMQuery.pkey)
            .limit(num_results)
            .offset(offset)
        )

        total_num_results = (await transaction.execute(sql_count)).scalar_one()
        result = (await transaction.execute(sql)).all()
        return Paginated[Query](
            items=[
                Query(
                    id=id,
                    corpus_name=corpus_name,
                    dataset_name=dataset_name,
                    text=text,
                    description=description,
                    num_relevant_documents=num_rel_docs,
                )
                for id, text, description, num_rel_docs, dataset_name in result
            ],
            offset=offset,
            total_num_items=total_num_results,
        )

    @get(path="/get_query")
    async def get_query(
        self,
        transaction: "AsyncSession",
        corpus_name: str,
        dataset_name: str,
        query_id: str,
    ) -> Query:
        """Return a single specific query.

        :param transaction: A DB transaction.
        :param corpus_name: The name of the corpus.
        :param dataset_name: The dataset name.
        :param query_id: The query ID.
        :raises HTTPException: When the query does not exist.
        :return: The query object.
        """
        sql = (
            select(
                ORMQuery,
                func.count(ORMQRel.document_pkey).filter(
                    ORMQRel.relevance >= ORMDataset.min_relevance
                ),
            )
            .join(ORMDataset)
            .join(ORMCorpus)
            .outerjoin(ORMQRel)
            .where(
                and_(
                    ORMQuery.id == query_id,
                    ORMCorpus.name == corpus_name,
                    ORMDataset.name == dataset_name,
                )
            )
            .group_by(ORMQuery.pkey)
        )

        try:
            db_query, num_rel_docs = (await transaction.execute(sql)).one()
        except NoResultFound:
            raise HTTPException(
                "Could not find the requested query.",
                status_code=HTTP_404_NOT_FOUND,
                extra={
                    "query_id": query_id,
                    "dataset_name": dataset_name,
                    "corpus_name": corpus_name,
                },
            )
        return Query(
            id=db_query.id,
            corpus_name=corpus_name,
            dataset_name=dataset_name,
            text=db_query.text,
            description=db_query.description,
            num_relevant_documents=num_rel_docs,
        )

    @get(path="/get_document")
    async def get_document(
        self, transaction: "AsyncSession", corpus_name: str, document_id: str
    ) -> Document:
        """Return a single specific document.

        :param transaction: A DB transaction.
        :param corpus_name: The corpus name.
        :param document_id: The document ID.
        :raises HTTPException: When the document does not exist.
        :return: The document object.
        """
        sql = (
            select(
                ORMDocument,
                func.count(ORMQRel.query_pkey).filter(
                    ORMQRel.relevance >= ORMDataset.min_relevance
                ),
            )
            .join(ORMCorpus)
            .outerjoin(ORMDataset)
            .outerjoin(ORMQRel)
            .where(ORMCorpus.name == corpus_name, ORMDocument.id == document_id)
        ).group_by(ORMDocument.pkey)

        try:
            db_document, num_rel_queries = (await transaction.execute(sql)).one()
        except NoResultFound as e:
            raise HTTPException(
                "Could not find the requested document.",
                status_code=HTTP_404_NOT_FOUND,
                extra={
                    "document_id": document_id,
                    "corpus_name": corpus_name,
                    "error_code": e.code,
                },
            )
        return Document(
            id=db_document.id,
            title=db_document.title,
            text=db_document.text,
            corpus_name=corpus_name,
            num_relevant_queries=num_rel_queries,
        )

    @get(path="/get_documents")
    async def get_documents(
        self,
        transaction: "AsyncSession",
        corpus_name: str,
        match: str | None = None,
        num_results: int = 10,
        offset: int = 0,
    ) -> Paginated[Document]:
        """List documents.

        :param transaction: A DB transaction.
        :param corpus_name: The name of the corpus.
        :param match: Return only documents matching this.
        :param num_results: How many documents to return.
        :param offset: Offset for pagination.
        :return: Paginated list of documents.
        """
        where_clauses = [ORMCorpus.name == corpus_name]
        if match is not None:
            where_clauses.append(
                ORMDocument.pkey.bool_op("@@@")(
                    func.paradedb.fuzzy_term(literal_column("'text'"), match)
                )
            )

        sql_count = (
            select(func.count())
            .select_from(ORMDocument)
            .join(ORMCorpus)
            .where(*where_clauses)
        )

        sql = (
            select(
                ORMDocument.id,
                ORMDocument.title,
                ORMDocument.text,
                func.count().label("count"),
            )
            .select_from(ORMQRel)
            .join(ORMQuery)
            .join(ORMDocument)
            .join(ORMDataset)
            .join(ORMCorpus)
            .where(*where_clauses, ORMQRel.relevance >= ORMDataset.min_relevance)
            .group_by(
                ORMDocument.pkey, ORMDocument.id, ORMDocument.title, ORMDocument.text
            )
            .order_by(desc(text("count")), ORMDocument.pkey)
            .limit(num_results)
            .offset(offset)
        )

        total_num_results = (await transaction.execute(sql_count)).scalar_one()
        result = (await transaction.execute(sql)).all()
        return Paginated[Document](
            items=[
                Document(
                    id=id,
                    corpus_name=corpus_name,
                    title=title,
                    text=text,
                    num_relevant_queries=num_rel_queries,
                )
                for id, title, text, num_rel_queries in result
            ],
            offset=offset,
            total_num_items=total_num_results,
        )

    @get(path="/search_documents")
    async def search_documents(
        self,
        transaction: "AsyncSession",
        q: str,
        corpus_name: list[str] | None = None,
        num_results: int = 10,
        offset: int = 0,
    ) -> Paginated[DocumentSearchHit]:
        """Search documents (using full-text search).

        :param transaction: A DB transaction.
        :param q: The search query.
        :param corpus_name: Search only within these corpora.
        :param num_results: How many hits to return.
        :param offset: Offset for pagination.
        :return: Paginated list of results, ordered by score.
        """
        where_clauses: list[SQLColumnExpression] = [ORMDocument.text.bool_op("@@@")(q)]
        if corpus_name is not None:
            corpus_cte = (
                select(ORMCorpus.pkey).where(ORMCorpus.name.in_(corpus_name)).cte()
            )

            # use ParadeDB's set filter: https://docs.paradedb.com/documentation/full-text/filtering#set-filter
            corpus_pkey_agg = select(
                func.concat(
                    "IN [",
                    func.string_agg(
                        func.cast(corpus_cte.c.pkey, VARCHAR), literal_column("' '")
                    ),
                    "]",
                )
            )
            where_clauses.append(
                ORMDocument.corpus_pkey.bool_op("@@@")(
                    corpus_pkey_agg.scalar_subquery()
                )
            )

        # count the total number of hits
        sql_count = select(func.count(ORMDocument.pkey)).where(and_(*where_clauses))

        # results for the current page only
        sql_results_sq = (
            select(
                ORMDocument.id,
                ORMDocument.corpus_pkey,
                func.paradedb.score(ORMDocument.pkey).label("score"),
                func.paradedb.snippet(ORMDocument.text, "<b>", "</b>", 500),
            )
            .where(and_(*where_clauses))
            .order_by(desc("score"))
            .order_by(ORMDocument.id)
            .offset(offset)
            .limit(num_results)
        ).subquery()

        # use a subquery to get the corpus names only for the current results
        sql_results = select(sql_results_sq, ORMCorpus.name).join(ORMCorpus)

        total_num_results = (await transaction.execute(sql_count)).scalar_one()
        results = (await transaction.execute(sql_results)).all()
        return Paginated[DocumentSearchHit](
            items=[
                DocumentSearchHit(
                    id=id,
                    corpus_name=corpus_name,
                    snippet=snippet,
                    score=score,
                )
                for id, _, score, snippet, corpus_name in results
            ],
            offset=offset,
            total_num_items=total_num_results,
        )

    @get(path="/get_qrels")
    async def get_qrels(
        self,
        transaction: "AsyncSession",
        corpus_name: str,
        document_id: str | None = None,
        dataset_name: str | None = None,
        query_id: str | None = None,
        match_query: str | None = None,
        match_document: str | None = None,
        num_results: int = 10,
        offset: int = 0,
    ) -> Paginated[QRel]:
        """Return query-document pairs annotated as relevant.

        :param transaction: A DB transaction.
        :param corpus_name: The corpus name.
        :param document_id: Return QRels for this document only.
        :param dataset_name: Return QRels for this dataset only.
        :param query_id: Return QRels for this query only.
        :param match_query: Return only queries matching this.
        :param match_document: Return only documents matching this.
        :param num_results: How many QRels to return.
        :param offset: Offset for pagination.
        :return: Paginated list of QRels, ordered by relevance.
        """
        where_clauses = [
            ORMCorpus.name == corpus_name,
            ORMQRel.relevance >= ORMDataset.min_relevance,
        ]
        if document_id is not None:
            where_clauses.append(ORMDocument.id == document_id)
        if dataset_name is not None:
            where_clauses.append(ORMDataset.name == dataset_name)
        if query_id is not None:
            where_clauses.append(ORMQuery.id == query_id)
        if match_query is not None:
            where_clauses.append(
                ORMQuery.pkey.bool_op("@@@")(
                    func.paradedb.fuzzy_term(literal_column("'text'"), match_query)
                )
            )
        if match_document is not None:
            where_clauses.append(
                ORMDocument.pkey.bool_op("@@@")(
                    func.paradedb.fuzzy_term(literal_column("'text'"), match_document)
                )
            )

        sql_count = (
            select(func.count())
            .select_from(ORMQRel)
            .join(ORMQuery)
            .join(ORMDocument)
            .join(ORMDataset)
            .join(ORMCorpus)
            .where(and_(*where_clauses))
        )

        sql = (
            select(ORMQRel)
            .join(ORMQuery)
            .join(ORMDocument)
            .join(ORMDataset)
            .join(ORMCorpus)
            .options(
                joinedload(ORMQRel.document).joinedload(ORMDocument.corpus),
                joinedload(ORMQRel.query)
                .joinedload(ORMQuery.dataset)
                .joinedload(ORMDataset.corpus),
            )
            .where(and_(*where_clauses))
            .order_by(ORMQRel.relevance.desc())
            .offset(offset)
            .limit(num_results)
        )

        total_num_results = (await transaction.execute(sql_count)).scalar_one()
        result = (await transaction.execute(sql)).scalars()
        return Paginated[QRel](
            items=[
                QRel(
                    query_info=QueryInfo(
                        id=qrel.query.id,
                        text=qrel.query.text,
                        description=qrel.query.description,
                    ),
                    document_info=DocumentInfo(
                        id=qrel.document.id,
                        title=qrel.document.title,
                        text=qrel.document.text,
                    ),
                    relevance=qrel.relevance,
                    corpus_name=qrel.document.corpus.name,
                    dataset_name=qrel.query.dataset.name,
                )
                for qrel in result
            ],
            offset=offset,
            total_num_items=total_num_results,
        )

    @delete(path="/remove_dataset")
    async def remove_dataset(
        self, transaction: "AsyncSession", corpus_name: str, dataset_name: str
    ) -> None:
        """Remove a dataset and its associated queries and QRels.

        :param transaction: A DB transaction.
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

        await transaction.execute(sql_del_qrels)
        await transaction.execute(sql_del_queries)
        await transaction.execute(sql_del_dataset)

    @delete(path="/remove_corpus")
    async def remove_corpus(
        self, transaction: "AsyncSession", corpus_name: str
    ) -> None:
        """Remove a corpus and its associated documents.

        Any associated datasets must be removed first.

        :param transaction: A DB transaction.
        :param corpus_name: The name of the corpus to remove.
        :raises HTTPException: When the corpus still has associated datasets.
        :raises HTTPException: When the corpus cannot be removed for other reasons.
        """
        sql_corpus = (
            select(ORMCorpus)
            .options(joinedload(ORMCorpus.datasets))
            .filter_by(name=corpus_name)
        )
        corpus = (await transaction.execute(sql_corpus)).unique().scalar_one()
        if len(corpus.datasets) > 0:
            raise HTTPException(
                "Associated datasets must be removed first.",
                status_code=HTTP_409_CONFLICT,
                extra={"corpus_name": corpus_name},
            )

        sql_del_documents = delete_(ORMDocument).filter_by(corpus_pkey=corpus.pkey)
        sql_del_corpus = delete_(ORMCorpus).filter_by(name=corpus_name)

        try:
            await transaction.execute(sql_del_documents)
            await transaction.execute(sql_del_corpus)
        except IntegrityError as e:
            raise HTTPException(
                "Failed to remove corpus.",
                status_code=HTTP_409_CONFLICT,
                extra={"corpus_name": corpus_name, "error_code": e.code},
            )
