"""Utilities."""

from typing import Callable, Any, Dict


def flatten_dict(item: Dict, cond_fn: Callable = None) -> Dict:
    """Flatten dictionary."""
    if isinstance(item, dict) and (cond_fn is None or cond_fn(item)):
        flattened = {}
        for key, value in item.items():
            if isinstance(value, dict) and (cond_fn is None or cond_fn(value)):
                for subkey, subvalue in value.items():
                    flattened[f"{key}.{subkey}"] = subvalue
            else:
                flattened[key] = value
        return flattened
    return item


def depth_map(map_fn: Callable[[Any], Any], item: Any) -> Any:
    """Depth-first map implementation on dictionary, tuple and list.

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
    if isinstance(item, dict):
        return map_fn({key: depth_map(map_fn, value) for key, value in item.items()})
    if isinstance(item, list):
        return map_fn([depth_map(map_fn, it) for it in item])
    if isinstance(item, tuple):
        return map_fn(tuple(depth_map(map_fn, it) for it in item))
    return map_fn(item)


def string_import(import_str: str) -> Any:
    """Import module attribute using import string.

    Parameters
    ----------
    import_str : str
        Full import string of the module attribute

    Returns
    -------
    Any
        A python object, class, function, etc.
    """
    parts = import_str.split(".")
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m
