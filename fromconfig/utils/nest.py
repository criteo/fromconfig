"""Nest Utilities."""

from collections.abc import Mapping, Iterable
import logging
from typing import Callable, Any, Dict


LOGGER = logging.getLogger(__name__)


def flatten_dict(item: Dict, cond_fn: Callable = None) -> Dict:
    """Flatten dictionary.

    Examples
    --------
    >>> import fromconfig
    >>> flat = fromconfig.utils.flatten_dict({"x": {"y": 1}})
    >>> flat["x.y"]
    1

    Parameters
    ----------
    item : Dict
        Dictionary to flatten
    cond_fn : Callable, optional
        If given and cond_fn(node) is False, stop flattening

    Returns
    -------
    Dict
    """
    if isinstance(item, Mapping) and (cond_fn is None or cond_fn(item)):
        flattened = {}
        for key, value in item.items():
            if isinstance(value, Mapping) and (cond_fn is None or cond_fn(value)):
                for subkey, subvalue in value.items():
                    flattened[f"{key}.{subkey}"] = subvalue
            else:
                flattened[key] = value
        return flattened
    return item


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

    # Check arguments types
    if not isinstance(item1, Mapping):
        raise TypeError(f"Expected type Mapping but got {type(item1)}")
    if not isinstance(item2, Mapping):
        raise TypeError(f"Expected type Mapping but got {type(item2)}")

    def _merge(it1: Any, it2: Any):
        """Recursive implementation."""
        if isinstance(it1, Mapping):
            if not isinstance(it2, Mapping):
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

            # Try to construct new instance of same type as it1
            try:
                return type(it1)(**merged)
            except Exception as e:  # pylint: disable=broad-except
                LOGGER.warning(f"Error while merging {it1} and {it2} ({e})")
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
    if isinstance(item, Mapping):
        kwargs = {key: depth_map(map_fn, value) for key, value in item.items()}
        try:
            return map_fn(type(item)(**kwargs))
        except Exception as e:  # pylint: disable=broad-except
            LOGGER.warning(f"Error while applying depth_map on {item} ({e})")
            return map_fn(kwargs)

    # If iterable, try to create new iterable with mapped args
    if not isinstance(item, str) and isinstance(item, Iterable):
        items = [depth_map(map_fn, it) for it in item]
        try:
            return map_fn(type(item)(*items))
        except Exception as e:  # pylint: disable=broad-except
            LOGGER.warning(f"Error while applying depth_map on {item} ({e})")
            return map_fn(items)

    return map_fn(item)
