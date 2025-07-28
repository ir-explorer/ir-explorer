"""Module for LLM-related functionality."""

import os
from typing import TYPE_CHECKING

from ollama import AsyncClient

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


OLLAMA_HOST = os.environ.get("OLLAMA_HOST")
OLLAMA_PORT = os.environ.get("OLLAMA_PORT")


async def provide_client() -> "AsyncGenerator[AsyncClient | None, None]":
    """Provide an asynchronous client for the Ollama API.

    If no Ollama host and/or port are set, yield None.

    :yield: The client (or None).
    """
    if OLLAMA_HOST is not None and OLLAMA_PORT is not None:
        yield AsyncClient(f"http://{OLLAMA_HOST}:{OLLAMA_PORT}")
    else:
        yield None
