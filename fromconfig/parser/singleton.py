"""Singleton parser."""

from collections import UserDict
from functools import partial
from typing import Any, Callable, Mapping

from fromconfig.core import Keys
from fromconfig.parser import base
from fromconfig.utils import depth_map, is_mapping, from_import_string, to_import_string


class _Singletons(UserDict):
    """Singleton register.

    Example
    -------
    >>> from fromconfig.parser import singleton
    >>> def constructor():
    ...     return {"foo": "bar"}
    >>> d1 = singleton("d1", constructor)
    >>> d2 = singleton("d1", constructor)  # constructor optional
    >>> id(d1) == id(d2)
    True
    """

    def __call__(self, key, constructor: Callable[[], Any] = None):
        """Get or create singleton."""
        if key not in self:
            if constructor is None:
                raise ValueError(f"Singleton {key} not found in {self}. Please specify constructor.")
            self[key] = constructor()
        return self[key]

    def __setitem__(self, key, value):
        if key in self:
            raise KeyError(f"Key {key} already in {self}. You must delete it first.")
        super().__setitem__(key, value)


singleton = _Singletons()


class SingletonParser(base.Parser):
    """Singleton parser.

    Examples
    --------
    >>> import fromconfig
    >>> config = {
    ...     "x": {
    ...         "_attr_": "dict",
    ...         "_singleton_": "my_dict",
    ...         "x": 1
    ...     },
    ...     "y": {
    ...         "_attr_": "dict",
    ...         "_singleton_": "my_dict",
    ...         "x": 1
    ...     }
    ... }
    >>> parser = fromconfig.parser.SingletonParser()
    >>> parsed = parser(config)
    >>> instance = fromconfig.fromconfig(parsed)
    >>> id(instance["x"]) == id(instance["y"])
    True
    """

    KEY = "_singleton_"

    def __call__(self, config: Mapping):
        """Parses config with _singleton_ key into valid config."""

        def _map_fn(item):
            if is_mapping(item) and self.KEY in item:
                key = item[self.KEY]
                name = item[Keys.ATTR]
                args = item.get(Keys.ARGS, [])
                kwargs = {key: value for key, value in item.items() if key not in (self.KEY, Keys.ATTR, Keys.ARGS)}
                attr = {Keys.ATTR.value: to_import_string(from_import_string), "name": name}
                constructor = {Keys.ATTR.value: to_import_string(partial), Keys.ARGS.value: [attr, *args], **kwargs}
                return {Keys.ATTR.value: to_import_string(singleton), "key": key, "constructor": constructor}
            return item

        return depth_map(_map_fn, config)
