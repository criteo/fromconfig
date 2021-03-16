"""Nest Utilities."""

import logging
from typing import Callable, Any, Mapping

from fromconfig.utils.types import is_mapping, is_pure_iterable


LOGGER = logging.getLogger(__name__)


def merge_dict(item1: Mapping, item2: Mapping, allow_override: bool = False) -> Mapping:
    """Merge item2 into item1.

    Examples
    --------
    >>> import fromconfig
    >>> merged = fromconfig.utils.merge_dict({"x": 1}, {"y": 2})
    >>> merged["x"]
    1
    >>> merged["y"]
    2

    Parameters
    ----------
    item1 : Mapping
        Reference mapping
    item2 : Mapping
        Override mapping
    allow_override : bool, optional
        If True, allow keys to be present in both item1 and item2

    Returns
    -------
    Mapping
    """

    def _merge(it1: Any, it2: Any):
        """Recursive implementation."""
        if is_mapping(it1):
            if not is_mapping(it2):
                raise TypeError(f"Incompatible types, {type(it2)} and {type(it2)}")

            # Build merged dictionary
            merged = {}
            for key in set(it1) | set(it2):
                if key in it1 and key in it2:
                    if not allow_override:
                        raise ValueError(f"Duplicate key found {key} and allow_override = False (not allowed)")
                    merged[key] = _merge(it1[key], it2[key])
                if key in it1 and key not in it2:
                    merged[key] = it1[key]
                if key not in it1 and key in it2:
                    merged[key] = it2[key]

            return merged

        return it2

    return _merge(item1, item2)


def depth_map(map_fn: Callable[[Any], Any], item: Any) -> Any:
    """Depth-first map implementation on dictionary, tuple and list.

    Examples
    --------
    >>> import fromconfig
    >>> def add_one(x):
    ...     return x + 1 if isinstance(x, int) else x
    >>> mapped = fromconfig.utils.depth_map(add_one, {"x": 1})
    >>> mapped["x"]
    2

    Parameters
    ----------
    map_fn : Callable[[Any], Any]
        Map Function to apply to item and its children
    item : Any
        Any python object

    Returns
    -------
    Any
        The result of applying map_fn to item and its children.
    """
    # If mapping, try to create new mapping with mapped kwargs
    if is_mapping(item):
        return map_fn({key: depth_map(map_fn, value) for key, value in item.items()})

    # If iterable, try to create new iterable with mapped args
    if is_pure_iterable(item):
        return map_fn([depth_map(map_fn, it) for it in item])

    return map_fn(item)
