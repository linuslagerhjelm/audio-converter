from collections.abc import Iterable

def flatten(outer_xs):
    """
    Flattens a nested list into a single list containing all the elements.

    Example: [1, [2, 3], 4, [[5]]] -> [1, 2, 3, 4, 5]

    Args:
        outer_xs (list): The list to flatten

    Returns:
        list: The flattened list.
    """
    def gen_flatten(xs):
        for x in xs:
            if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
                yield from flatten(x)
            else:
                yield x
    return list(gen_flatten(outer_xs))