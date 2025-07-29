from typing import TYPE_CHECKING

from db import provide_transaction
from db.schema import ORMCorpus, ORMDocument
from db.util import escape_search_query
from litestar import Controller, get
from litestar.di import Provide
from models import (
    AvailableOptions,
    DocumentSearchHit,
    Paginated,
)
from sqlalchemy import (
    VARCHAR,
    Integer,
    SQLColumnExpression,
    and_,
    desc,
    func,
    literal_column,
    select,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class SearchController(Controller):
    """Controller that handles search-related API endpoints."""

    dependencies = {"db_transaction": Provide(provide_transaction)}

    @get(path="/get_available_languages", cache=True)
    def get_available_languages(self) -> list[str]:
        """List all corpus languages supported by the DB engine (for full-text search).

        :return: All available languages.
        """
        # currently, paradedb does not support configuration based on a language column,
        # so, for now, only english is supported
        # https://github.com/paradedb/paradedb/issues/1793
        return ["English"]

    @get(path="/get_available_options", cache=True)
    async def get_available_options(
        self, db_transaction: "AsyncSession"
    ) -> AvailableOptions:
        """Get available options for all settings.

        :param db_transaction: A DB transaction.
        :return: The available options.
        """
        sql = select(ORMCorpus.name)
        result = (await db_transaction.execute(sql)).scalars()
        return AvailableOptions(query_languages=["English"], corpus_names=list(result))

    @get(path="/search_documents", cache=True)
    async def search_documents(
        self,
        db_transaction: "AsyncSession",
        q: str,
        corpus_name: list[str] | None = None,
        num_results: int = 10,
        offset: int = 0,
    ) -> Paginated[DocumentSearchHit]:
        """Search documents (using full-text search).

        :param db_transaction: A DB transaction.
        :param q: The search query.
        :param corpus_name: Search only within these corpora.
        :param num_results: How many hits to return.
        :param offset: Offset for pagination.
        :return: Paginated list of results, ordered by score.
        """
        where_clause: list[SQLColumnExpression] = [
            ORMDocument.text.bool_op("@@@")(escape_search_query(q))
        ]
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
            where_clause.append(
                ORMDocument.corpus_pkey.bool_op("@@@")(
                    corpus_pkey_agg.scalar_subquery()
                )
            )

        # count the total number of hits
        sql_count = select(func.count(ORMDocument.pkey)).where(and_(*where_clause))

        # results for the current page only
        sql_results_sq = (
            select(
                ORMDocument.id,
                ORMDocument.corpus_pkey,
                func.paradedb.score(ORMDocument.pkey).label("score"),
                func.paradedb.snippet(
                    ORMDocument.text,
                    literal_column("'<b>'"),
                    literal_column("'</b>'"),
                    literal_column("500", Integer),
                ),
            )
            .where(and_(*where_clause))
            .order_by(desc("score"))
            .order_by(ORMDocument.id)
            .offset(offset)
            .limit(num_results)
        ).subquery()

        # use a subquery to get the corpus names only for the current results
        sql_results = select(sql_results_sq, ORMCorpus.name).join(ORMCorpus)

        total_num_results = (await db_transaction.execute(sql_count)).scalar_one()
        results = (await db_transaction.execute(sql_results)).all()
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
