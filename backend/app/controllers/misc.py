from typing import TYPE_CHECKING

from db import provide_transaction
from db.schema import ORMCorpus
from litestar import Controller, get
from litestar.di import Provide
from llm import provide_client
from models import (
    AvailableOptions,
)

# litestar needs the type outside of the type checking block
from openai import AsyncOpenAI  # noqa: TC002
from sqlalchemy import (
    select,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class MiscController(Controller):
    """Controller that handles miscellaneous API endpoints."""

    dependencies = {
        "db_transaction": Provide(provide_transaction),
        "openai_client": Provide(provide_client),
    }

    @get(path="/get_available_languages")
    def get_available_languages(self) -> list[str]:
        """List all corpus languages supported by the DB engine (for full-text search).

        :return: All available languages.
        """
        # currently, paradedb does not support configuration based on a language column,
        # so, for now, only english is supported
        # https://github.com/paradedb/paradedb/issues/1793
        return ["English"]

    @get(path="/get_available_options")
    async def get_available_options(
        self,
        db_transaction: "AsyncSession",
        openai_client: AsyncOpenAI | None,
    ) -> AvailableOptions:
        """Get available options for all settings.

        :param db_transaction: A DB transaction.
        :param openai_client: An OpenAI client.
        :return: The available options.
        """
        model_names = []
        if openai_client is not None:
            for t, item in await openai_client.models.list():
                if t == "data" and item is not None:
                    model_names.extend([model.id for model in item])

        sql = select(ORMCorpus.name)
        result = (await db_transaction.execute(sql)).scalars()
        return AvailableOptions(
            query_languages=["English"],
            corpus_names=list(result),
            model_names=model_names,
        )
