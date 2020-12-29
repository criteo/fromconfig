"""Singleton parser."""

from typing import Mapping

from fromconfig import Keys
from fromconfig.utils import depth_map, is_mapping
from fromconfig.parsers.base import Parser


class SingletonParser(Parser):
    """Singleton parser."""

    KEY = "_singleton_"

    def __call__(self, config: Mapping):
        """Parses config with _singleton_ key into valid config."""

        def _map_fn(item):
            if is_mapping(item) and self.KEY in item:
                key = item[self.Key]
                name = item.get(Keys.ATTR)
                args = item.get(Keys.ARGS, [])
                kwargs = {key: value for key, value in item.items() if key not in (self.KEY, Keys.ATTR, Keys.ARGS)}
                constructor = {Keys.ATTR: "functools.partial", Keys.ARGS: [name, *args] if name else args, **kwargs}
                return {Keys.ATTR: "fromconfig.singleton", "key": key, "constructor": constructor}
            return item

        return depth_map(_map_fn, config)
