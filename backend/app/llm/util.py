import os
from string import Formatter

LLM_PROMPT_SUMMARY = os.environ.get("LLM_PROMPT_SUMMARY")


def get_summary_prompt(text: str, title: str | None) -> str:
    """Assemble the LLM input string for document summarization.

    :param text: The document text.
    :param title: The document title (if any).
    :raises RuntimeError: When no prompt template exists.
    :raises RuntimeError: When the prompt template is malformed.
    :return: The LLM input.
    """
    if LLM_PROMPT_SUMMARY is None:
        raise RuntimeError("No LLM summary prompt configured.")

    # no placeholders other than "title" and "text" may appear
    placeholders = {
        name
        for _, name, _, _ in Formatter().parse(LLM_PROMPT_SUMMARY)
        if name is not None
    }
    if len(placeholders - {"title", "text"}) > 0:
        raise RuntimeError("LLM summary prompt is malformed.")

    return LLM_PROMPT_SUMMARY.format(text=text, title=title)
