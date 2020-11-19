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


def child_map(map_fn: Callable[[Any], Any], item: Any, stop_fn: Callable[[Any], bool] = None) -> Any:
    """Map Function on item, recursively on children.

    Parameters
    ----------
    map_fn : Callable[[Any], Any]
        Map Function to apply to item and its children
    item : Any
        Any python object
    stop_fn : Callable[[Any], bool], optional
        When specified and stop_fn(item) is True, stop recursive call.

    Returns
    -------
    Any
        The result of applying map_fn to item and its children.
    """
    if stop_fn and stop_fn(item):
        return item
    if isinstance(item, dict):
        return map_fn({key: child_map(map_fn, value, stop_fn) for key, value in item.items()})
    if isinstance(item, list):
        return map_fn([child_map(map_fn, it, stop_fn) for it in item])
    if isinstance(item, tuple):
        return map_fn(tuple(child_map(map_fn, it, stop_fn) for it in item))
    return map_fn(item)


def import_from_string(import_str: str) -> Any:
    """Import module member using import string.

    Parameters
    ----------
    import_str : str
        Full import string of the module member

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
