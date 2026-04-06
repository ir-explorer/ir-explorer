# escape ' and ", as the same effect can be achieved with +,
# i.e., "term1 term2" is the same as term1+term2
TRANSLATE_ILLEGAL_CHARS = str.maketrans(
    {
        f"{c}": rf"\{c}"
        for c in ["^", "{", "}", "[", "]", "(", ")", "<", ">", "'", '"', "`"]
    }
)


def escape_search_query(q: str) -> str:
    """Escape an input search string for ParadeDB.

    According to: https://docs.paradedb.com/documentation/full-text/overview#special-characters

    :param q: The search query.
    :return: The escaped query.
    """
    return q.translate(TRANSLATE_ILLEGAL_CHARS)
