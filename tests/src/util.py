def list_of_dicts_equal(l1, l2) -> bool:
    """Check whether two lists contain the same dictionaries, disregarding the order.

    :param d1: The first list.
    :param d2: The seconds list.
    :return: Whether they are equal.
    """

    def key(x):
        return list(x.values())

    return sorted(l1, key=key) == sorted(l2, key=key)
