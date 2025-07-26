def list_of_dicts_equal(
    l1: list[dict[str, str | int | float]],
    l2: list[dict[str, str | int | float]],
    ignore_keys: set[str] | None = None,
) -> bool:
    """Check whether two lists contain the same dictionaries, disregarding the order.

    :param d1: The first list.
    :param d2: The seconds list.
    :param ignore_keys: Dictionary keys in this set will be ignored.
    :return: Whether they are equal.
    """
    if ignore_keys is not None:
        l1_ = [{k: v for k, v in x.items() if k not in ignore_keys} for x in l1]
        l2_ = [{k: v for k, v in x.items() if k not in ignore_keys} for x in l2]
    else:
        l1_, l2_ = l1, l2

    def sort_key(x):
        return list(x.values())

    return sorted(l1_, key=sort_key) == sorted(l2_, key=sort_key)
