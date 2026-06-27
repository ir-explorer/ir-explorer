from collections.abc import Mapping, Sequence, Set
from typing import Union

NestedMapping = Mapping[str, Union[str, int, float, "NestedMapping"]]


def flatten(
    d: NestedMapping, key_prefix: str | None = None
) -> dict[str, str | int | float]:
    """Flatten a nested dictionary.

    :param d: The nested dictionary.
    :param key_prefix: Prefix used for recursion.
    :return: The flattened dictionary.
    """
    result = []
    for k, v in d.items():
        k_ = key_prefix + "_" + k if key_prefix else k
        if isinstance(v, Mapping):
            result.extend(flatten(v, k_).items())
        else:
            result.append((k_, v))
    return dict(result)


def list_of_dicts_equal(
    l1: Sequence[NestedMapping],
    l2: Sequence[NestedMapping],
    ignore_keys: Set[str] = frozenset(),
) -> bool:
    """Check whether two lists contain the same dictionaries, disregarding the order.

    Flattens nested dictionaries.

    :param l1: The first list.
    :param l2: The seconds list.
    :param ignore_keys: Dictionary keys in this set will be ignored.
    :return: Whether they are equal.
    """
    l1_ = [flatten({k: v for k, v in x.items() if k not in ignore_keys}) for x in l1]
    l2_ = [flatten({k: v for k, v in x.items() if k not in ignore_keys}) for x in l2]

    def sort_key(x: Mapping[str, str | int | float]) -> str:
        return repr(tuple(x.values()))

    return sorted(l1_, key=sort_key) == sorted(l2_, key=sort_key)
