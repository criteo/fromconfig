"""Reference Parser."""

from typing import Any, Mapping, List, Union
import functools
import operator

from fromconfig.parser import base
from fromconfig.utils import is_mapping, is_pure_iterable


class ReferenceParser(base.Parser):
    """Reference Parser.

    Examples
    --------
    >>> import fromconfig
    >>> parser = fromconfig.parser.ReferenceParser()
    >>> config = {"params": {"x": 1}, "y": "@params.x"}
    >>> parsed = parser(config)
    >>> parsed["y"]
    1

    The reference parser is convenient to compose different configs
    dynamically.

    >>> import fromconfig
    >>> param1 = {"params": {"x": 1}}
    >>> param2 = {"params": {"x": 2}}
    >>> config = {"model": {"x": "@params.x"}}
    >>> parser = fromconfig.parser.ReferenceParser()
    >>> parser({**config, **param1})["model"]["x"]
    1
    >>> parser({**config, **param2})["model"]["x"]
    2
    """

    PREFIX = "@"

    def __call__(self, config: Mapping):

        references = set()

        def _resolve(item, visited: List[str]):
            if is_mapping(item):
                return {_resolve(key, visited): _resolve(value, visited) for key, value in item.items()}

            if is_pure_iterable(item):
                return [_resolve(it, visited) for it in item]

            if is_reference(item):
                references.add(item)
                if item in visited:
                    raise ValueError(f"Found cycle {visited}")
                visited_copy = visited + [item]  # Copy when "branching"
                keys = reference_to_keys(item)
                return _resolve(functools.reduce(operator.getitem, keys, config), visited_copy)

            return item

        return _resolve(config, [])


def is_reference(item: Any) -> bool:
    """Return True if item is a string starting with the "@".

    Parameters
    ----------
    item : Any
        Any python object

    Returns
    -------
    bool
    """
    if hasattr(item, "startswith"):
        return item.startswith(ReferenceParser.PREFIX)
    return False


def reference_to_keys(reference: str) -> List[Union[str, int]]:
    """Get keys from a reference string.

    Parameters
    ----------
    reference : str
        A reference string

    Returns
    -------
    List[Union[str, int]]
    """
    parts = []  # type: List[Union[str, int]]
    for part in reference.lstrip(ReferenceParser.PREFIX).split("."):
        if part.endswith("]"):
            left = part.find("[")
            parts.append(part[:left])
            parts.append(int(part[left + 1 : -1]))
        else:
            parts.append(part)
    return parts
