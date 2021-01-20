"""Singleton parser."""

from typing import Mapping
from functools import partial

from fromconfig.core import Keys
from fromconfig.parser import base
from fromconfig.utils import depth_map, is_mapping, from_import_string, to_import_string


class SingletonParser(base.Parser):
    """Singleton parser."""

    KEY = "_singleton_"

    def __call__(self, config: Mapping):
        """Parses config with _singleton_ key into valid config."""

        def _map_fn(item):
            if is_mapping(item) and self.KEY in item:
                key = item[self.KEY]
                name = item[Keys.ATTR]
                args = item.get(Keys.ARGS, [])
                kwargs = {key: value for key, value in item.items() if key not in (self.KEY, Keys.ATTR, Keys.ARGS)}
                attr = {Keys.ATTR: to_import_string(from_import_string), "name": name}
                constructor = {Keys.ATTR: to_import_string(partial), Keys.ARGS: [attr, *args], **kwargs}
                return {Keys.ATTR: "singleton", "key": key, "constructor": constructor}
            return item

        return depth_map(_map_fn, config)
