"""Container utilities."""

from collections.abc import Mapping, Iterable
from collections import UserDict
import logging


LOGGER = logging.getLogger(__name__)


def is_mapping(item) -> bool:
    return item is not None and isinstance(item, Mapping)


def is_iterable(item) -> bool:
    return item is not None and not isinstance(item, str) and isinstance(item, Iterable) and not is_mapping(item)


def try_init(cls, default_cls, *args, **kwargs):
    """Initialize cls or default_cls with args and kwargs."""
    try:
        return cls(*args, **kwargs)
    except Exception as e:  # pylint: disable=broad-except
        LOGGER.warning(f"Unable to instantiate {cls} with {args} and {kwargs} ({e})")
        return default_cls(*args, **kwargs)


class WeakImmutableDict(UserDict):
    """Cannot mutate keys already present in a dictionary."""

    def __setitem__(self, key, value):
        if key in self:
            raise KeyError(f"Key {key} already in {self}. You must delete it first.")
        super().__setitem__(key, value)
