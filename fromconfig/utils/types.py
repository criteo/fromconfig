"""Types utilities."""

from collections.abc import Mapping, Iterable
import logging


LOGGER = logging.getLogger(__name__)


def is_mapping(item) -> bool:
    return item is not None and isinstance(item, Mapping)


def is_pure_iterable(item) -> bool:
    return item is not None and not isinstance(item, str) and isinstance(item, Iterable) and not is_mapping(item)
