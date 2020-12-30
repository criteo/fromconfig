"""Reference Parser."""

from typing import Any, Mapping, Iterable

from fromconfig.core import Keys
from fromconfig.parser import base
from fromconfig.utils import flatten_dict, depth_map


class ReferenceParser(base.Parser):
    """Reference Parser.

    Examples
    --------
    >>> import fromconfig
    >>> parser = fromconfig.parser.ReferenceParser()
    >>> config = {"x": 1, "y": "@x"}
    >>> parsed = parser(config)
    >>> parsed["y"]
    1
    """

    PREFIX = "@"

    def __init__(self, keys: Iterable[str] = None, allow_missing: bool = False):
        self.keys = keys
        self.allow_missing = allow_missing

    def __call__(self, config: Mapping):
        # Extract references from config
        def _cond_fn(cfg):
            return not any(key in cfg for key in Keys)

        if self.keys is not None:
            references = flatten_dict({key: value for key, value in config.items() if key in self.keys}, _cond_fn)
        else:
            references = flatten_dict(config, _cond_fn)

        def _map_fn(item):
            if self.is_reference(item):
                ref = self.get_reference(item)
                if ref in references:
                    return references[ref]
                if self.allow_missing:
                    return item
                raise KeyError(f"Reference {ref} not found in references {references}")
            return item

        # TODO: more deterministic (check for cycles)
        for _ in range(len(references)):
            config = depth_map(_map_fn, config)

        return config

    def is_reference(self, ref: Any) -> bool:
        if hasattr(ref, "startswith"):
            return ref.startswith(self.PREFIX)
        return False

    def get_reference(self, ref: str) -> str:
        if not self.is_reference(ref):
            raise ValueError(f"{ref} is not a valid reference.")
        return ref[1:]  # Remove PREFIX
