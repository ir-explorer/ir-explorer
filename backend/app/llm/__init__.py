"""Module for LLM-related functionality."""

import os
from typing import TYPE_CHECKING

from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_503_SERVICE_UNAVAILABLE
from openai import AsyncOpenAI

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


OPENAI_API_ENDPOINT = os.environ.get("OPENAI_API_ENDPOINT")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


async def ensure_model_available(
    openai_client: AsyncOpenAI | None, model_name: str
) -> AsyncOpenAI:
    """Check whether a requested model is available.

    :param openai_client: An OpenAI client.
    :param model_name: The requested model name.
    :raises HTTPException: When LLM services or the requested model are unavailable.
    :return: The validated OpenAI client.
    """
    if openai_client is None:
        raise HTTPException(
            "LLM services not available.",
            status_code=HTTP_503_SERVICE_UNAVAILABLE,
        )

    try:
        available_model_names = [
            model.id for model in (await openai_client.models.list()).data
        ]
    except Exception as e:
        raise HTTPException(
            "LLM list not available.",
            status_code=HTTP_503_SERVICE_UNAVAILABLE,
            extra={"error": str(e)},
        )

    if model_name not in available_model_names:
        raise HTTPException(
            "Requested model is not available.",
            status_code=HTTP_503_SERVICE_UNAVAILABLE,
            extra={
                "model_name": model_name,
                "available_model_names": available_model_names,
            },
        )

    return openai_client


async def provide_client() -> "AsyncGenerator[AsyncOpenAI | None, None]":
    """Provide an asynchronous client for the OpenAI API.

    If no endpoint is set, yield None.

    :yield: The client (or None).
    """
    if OPENAI_API_ENDPOINT is not None:
        yield AsyncOpenAI(base_url=OPENAI_API_ENDPOINT, api_key=OPENAI_API_KEY)
    else:
        yield None
