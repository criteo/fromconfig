"""Reference Parser."""

from typing import Any, Mapping

from fromconfig.core import Keys
from fromconfig.utils import flatten_dict, depth_map
from fromconfig.parser import base


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

    def __call__(self, config: Mapping):
        references = flatten_dict(config, lambda cfg: not any(key in cfg for key in Keys))

        def _map_fn(item):
            if self.is_reference(item):
                return references[self.get_reference(item)]
            return item

        # TODO: more deterministic (check for cycles)
        for _ in range(len(references) - 1):
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
