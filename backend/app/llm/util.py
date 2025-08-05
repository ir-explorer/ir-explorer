import os
from string import Formatter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

LLM_PROMPT_SUMMARY = os.environ.get("LLM_PROMPT_SUMMARY")
LLM_PROMPT_RAG = os.environ.get("LLM_PROMPT_RAG")
LLM_PROMPT_RAG_DOCUMENT = os.environ.get("LLM_PROMPT_RAG_DOCUMENT")


def has_valid_placeholders(s: str, allowed_placeholders: set[str]) -> bool:
    """Check whether a provided format string contains only the allowed placeholders.

    :param s: The format string to check.
    :param allowed_placeholders: The allowed placeholders.
    :return: Whether the format string is valid.
    """
    placeholders_in_s = {
        name for _, name, _, _ in Formatter().parse(s) if name is not None
    }
    return len(placeholders_in_s - allowed_placeholders) == 0


def get_summary_prompt(text: str, title: str | None) -> str:
    """Assemble the LLM input string for document summarization.

    :param text: The document text.
    :param title: The document title (if any).
    :raises RuntimeError: When no prompt template exists.
    :raises RuntimeError: When the prompt template is malformed.
    :return: The LLM input.
    """
    if LLM_PROMPT_SUMMARY is None:
        raise RuntimeError("No LLM summary prompt template configured.")
    if not has_valid_placeholders(LLM_PROMPT_SUMMARY, {"title", "text"}):
        raise RuntimeError("LLM summary prompt template is malformed.")

    return LLM_PROMPT_SUMMARY.format(text=text, title=title)


def get_rag_prompt(q: str, documents: "Sequence[tuple[str | None, str]]") -> str:
    """Assemble the LLM input string for RAG.

    :param q: The query/question.
    :param documents: Titles and texts of documents.
    :raises RuntimeError: When no prompt template exists.
    :raises RuntimeError: When the prompt template is malformed.
    :return: The LLM input.
    """
    if LLM_PROMPT_RAG is None or LLM_PROMPT_RAG_DOCUMENT is None:
        raise RuntimeError("No LLM RAG prompt template configured.")
    if not has_valid_placeholders(
        LLM_PROMPT_RAG, {"question", "context"}
    ) or not has_valid_placeholders(
        LLM_PROMPT_RAG_DOCUMENT, {"docno", "title", "text"}
    ):
        raise RuntimeError("LLM RAG prompt template is malformed.")

    doc_prompts = [
        LLM_PROMPT_RAG_DOCUMENT.format(docno=i + 1, title=title, text=text)
        for i, (title, text) in enumerate(documents)
    ]
    return LLM_PROMPT_RAG.format(question=q, context="\n\n".join(doc_prompts))
