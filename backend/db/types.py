from typing import Any

from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.types import TypeDecorator


class TSVectorType(TypeDecorator):
    """TSVector type for full-text search.

    Adapted from:
    https://github.com/kvesteri/sqlalchemy-utils/blob/baf53cd1a3e779fc127010543fed53cf4a97fe16/sqlalchemy_utils/types/ts_vector.py
    """

    impl = TSVECTOR
    cache_ok = True

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize a TSVector type.

        :param args: Columns.
        :param kwargs: Options.
        """
        self.columns = args
        self.options = kwargs
        super().__init__()
