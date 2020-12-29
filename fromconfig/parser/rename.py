"""Rename parser."""

from typing import Dict, Mapping

from fromconfig.utils import depth_map, is_mapping
from fromconfig.parser import base


class RenameParser(base.Parser):
    """Rename Keys parser."""

    def __init__(self, renames: Dict[str, str]):
        self.renames = renames

    def __call__(self, config: Mapping):
        """Rename keys in config."""

        def _map_fn(item):
            if is_mapping(item) and any(key in item for key in self.renames):
                return {self.renames.get(key, key): value for key, value in item.items()}
            return item

        return depth_map(_map_fn, config)
