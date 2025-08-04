import os
from collections.abc import Sequence
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
        raise RuntimeError("LLM summary prompt template is malformed.")

    return LLM_PROMPT_SUMMARY.format(text=text, title=title)


def get_rag_prompt(q: str, documents: Sequence[tuple[str | None, str]]) -> str:
    """Assemble the LLM input string for RAG.

    :param q: The query/question.
    :param documents: Titles and texts of documents.
    :return: The LLM input.
    """
    doc_prompt_tpl = """---------- DOCUMENT {docno}
    Title: {title}

    Text: {text}
    ---------- END: DOCUMENT {docno}
    """

    prompt_tpl = """Answer the following question given the context documents below.

    Question: {question}

    Context documents:

    """

    prompt = prompt_tpl.format(question=q)
    for i, (title, text) in enumerate(documents):
        prompt += doc_prompt_tpl.format(docno=i + 1, title=title, text=text)

    return prompt
