from collections.abc import MutableMapping
from typing import Union

NestedDict = dict[str, Union[str, int, float, "NestedDict"]]


def flatten(
    d: NestedDict, key_prefix: str | None = None
) -> dict[str, str | int | float]:
    """Flatten a nested dictionary.

    :param d: The nested dictionary.
    :param key_prefix: Prefix used for recursion.
    :return: The flattened dictionary.
    """
    result = []
    for k, v in d.items():
        k_ = key_prefix + "_" + k if key_prefix else k
        if isinstance(v, MutableMapping):
            result.extend(flatten(v, k_).items())
        else:
            result.append((k_, v))
    return dict(result)


def list_of_dicts_equal(
    l1: list[NestedDict],
    l2: list[NestedDict],
    ignore_keys: set[str] = {},
) -> bool:
    """Check whether two lists contain the same dictionaries, disregarding the order.

    Flattens nested dictionaries.

    :param d1: The first list.
    :param d2: The seconds list.
    :param ignore_keys: Dictionary keys in this set will be ignored.
    :return: Whether they are equal.
    """
    l1_ = [flatten({k: v for k, v in x.items() if k not in ignore_keys}) for x in l1]
    l2_ = [flatten({k: v for k, v in x.items() if k not in ignore_keys}) for x in l2]

    def sort_key(x):
        return list(x.values())

    return sorted(l1_, key=sort_key) == sorted(l2_, key=sort_key)
