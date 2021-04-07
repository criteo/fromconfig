"""Nest Utilities."""

import logging
from typing import Callable, Dict, Any, Mapping, List, Tuple, Iterable, Union

from fromconfig.utils.types import is_mapping, is_pure_iterable


LOGGER = logging.getLogger(__name__)


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


def merge_dict(item1: Mapping, item2: Mapping, allow_override: bool = True) -> Mapping:
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


def flatten(config: Any) -> List[Tuple[str, Any]]:
    """Flatten dictionary into a list of tuples key, value.


    Example
    -------
    >>> import fromconfig
    >>> d = {"x": {"y": 0}}
    >>> fromconfig.utils.flatten(d)
    [('x.y', 0)]

    Parameters
    ----------
    config : Any
        Typically a dictionary (possibly nested)

    Returns
    -------
    List[Tuple[Optional[str], Any]]
        Each tuple is a flattened key with the corresponding value.
    """

    def _flatten(item) -> List[Tuple[List[Union[str, int]], Any]]:
        if is_mapping(item):
            result = []
            for key, values in item.items():
                if "." in key:
                    raise ValueError(f"Key {key} already has a `.`, unable to flatten.")
                for subkeys, value in values:
                    result.append(([str(key)] + subkeys, value))
            return result

        if is_pure_iterable(item):
            result = []
            for idx, it in enumerate(item):
                for subkeys, value in it:
                    result.append(([idx] + subkeys, value))
            return result

        return [([], item)]

    flattened = depth_map(_flatten, config)
    return [(_to_dotlist(key), value) for key, value in flattened]


def expand(flat: Iterable[Tuple[str, Any]]):
    """Expand flat dictionary into nested dictionary.

    Example
    -------
    >>> import fromconfig
    >>> d = {"x.y": 0}
    >>> fromconfig.utils.expand(d.items())
    {'x': {'y': 0}}

    Parameters
    ----------
    flat : Iterable[Tuple[Optional[str], Any]]
        Iterable of flat keys, value
    """

    def _expand(it: List[Tuple[List[Union[str, int]], Any]]) -> Dict:
        # Recursive step
        result = {}  # type: ignore
        for keys, value in it:
            if not keys:
                if None in result:
                    raise KeyError("More than one pure value found (not allowed)")
                result[None] = value
            else:
                key = keys[0]
                value = _expand([(keys[1:], value)])
                result[key] = merge_dict(value, result.get(key, {}))
        return result

    def _normalize(it):
        if is_mapping(it) and any(isinstance(key, int) for key in it):
            return [it[idx] for idx in range(len(it))]
        if is_mapping(it) and any(key is None for key in it):
            if len(it) > 1:
                raise KeyError("More than one pure value found (not allowed)")
            return it[None]
        return it

    return depth_map(_normalize, _expand([(_from_dotlist(dotlist), value) for dotlist, value in flat]))


def _to_dotlist(keys: List[Union[str, int]]) -> str:
    """Convert list of keys to dot-list.

    Parameters
    ----------
    keys : List[Union[str, int]]
        List of keys.
    """
    dotlist = ""
    for key in keys:
        if isinstance(key, str):
            dotlist = key if not dotlist else f"{dotlist}.{key}"
        elif isinstance(key, int):
            dotlist = f"{dotlist}[{key}]"
        else:
            raise TypeError(f"Unsupported key type {type(key)}")
    return dotlist


def _from_dotlist(dotlist: str) -> List[Union[str, int]]:
    """Convert dot-list to list of keys.

    Parameters
    ----------
    dotlist : str
        Dot-List
    """
    keys: List[Union[str, int]] = []
    for item in dotlist.split("."):
        for it in item.split("["):
            if it.endswith("]"):
                keys.append(int(it.rstrip("]")))
            else:
                keys.append(it)
    return keys
