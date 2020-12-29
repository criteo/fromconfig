"""Rename parser."""

from collections.abc import Mapping
from typing import Dict

from fromconfig.utils import depth_map
from fromconfig.parsers.base import Parser


class RenameParser(Parser):
    """Rename Keys parser."""

    def __init__(self, renames: Dict[str, str]):
        self.renames = renames

    def __call__(self, config):
        """Rename keys in config."""

        def _map_fn(item):
            if isinstance(item, Mapping) and any(key in item for key in self.renames):
                return {self.renames.get(key, key): value for key, value in item.items()}
            return item

        return depth_map(_map_fn, config)
