"""Singleton Functionality."""

from collections.abc import MutableMapping
from typing import Any, Callable
from fromconfig.core.register import register


class _Singletons(MutableMapping):
    """Singleton register."""

    def __init__(self):
        self._singletons = {}

    def __getitem__(self, item):
        return self._singletons[item]

    def __setitem__(self, key, value):
        if key in self._singletons:
            raise KeyError(f"Key {key} already in {self}. You must delete it first.")
        self._singletons[key] = value

    def __delitem__(self, key):
        self._singletons.__delitem__(key)

    def __iter__(self):
        yield from self._singletons

    def __len__(self):
        return len(self._singletons)

    def __call__(self, key, constructor: Callable[[], Any] = None):
        """Get or create singleton."""
        if key not in self:
            if not constructor:
                raise ValueError(f"Singleton {key} not found in {self}. Please specify constructor.")
            self[key] = constructor()
        return self[key]


singleton = register("singleton", _Singletons())
