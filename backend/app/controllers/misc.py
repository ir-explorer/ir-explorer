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
from ollama import AsyncClient  # noqa: TC002
from sqlalchemy import (
    select,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class MiscController(Controller):
    """Controller that handles miscellaneous API endpoints."""

    dependencies = {
        "db_transaction": Provide(provide_transaction),
        "ollama_client": Provide(provide_client),
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
        ollama_client: AsyncClient | None,
    ) -> AvailableOptions:
        """Get available options for all settings.

        :param db_transaction: A DB transaction.
        :param ollama_client: An Ollama client.
        :return: The available options.
        """
        if ollama_client is None:
            model_names = []
        else:
            model_names = [
                model["model"] for model in (await ollama_client.list()).models
            ]

        sql = select(ORMCorpus.name)
        result = (await db_transaction.execute(sql)).scalars()
        return AvailableOptions(
            query_languages=["English"],
            corpus_names=list(result),
            model_names=model_names,
        )
