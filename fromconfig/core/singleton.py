"""Singleton Functionality."""

from typing import Any, Callable

from fromconfig.core.register import register
from fromconfig.utils import ImmutableDict


class _Singletons(ImmutableDict):
    """Singleton register."""

    def __call__(self, key, constructor: Callable[[], Any] = None):
        """Get or create singleton."""
        if key not in self:
            if not constructor:
                raise ValueError(f"Singleton {key} not found in {self}. Please specify constructor.")
            self[key] = constructor()
        return self[key]


singleton = register("singleton", _Singletons())
