"""Module for LLM-related functionality."""

import os
from typing import TYPE_CHECKING

from openai import AsyncOpenAI

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


OPENAI_API_ENDPOINT = os.environ.get("OPENAI_API_ENDPOINT")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


async def provide_client() -> "AsyncGenerator[AsyncOpenAI | None, None]":
    """Provide an asynchronous client for the OpenAI API.

    If no endpoint is set, yield None.

    :yield: The client (or None).
    """
    if OPENAI_API_ENDPOINT is not None:
        yield AsyncOpenAI(base_url=OPENAI_API_ENDPOINT, api_key=OPENAI_API_KEY)
    else:
        yield None
