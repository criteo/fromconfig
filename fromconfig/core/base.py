"""Base functionality."""

from abc import ABC, abstractclassmethod
from collections.abc import Mapping, Iterable
import logging

from fromconfig.utils import StrEnum
from fromconfig.core.register import register


LOGGER = logging.getLogger(__name__)


class Keys(StrEnum):
    """Special Keys."""

    ATTR = "_attr_"
    ARGS = "_args_"


class FromConfig(ABC):
    """Abstract class for custom from_config implementations."""

    @abstractclassmethod
    def fromconfig(cls, config: Mapping):
        raise NotImplementedError()


def fromconfig(config, safe: bool = False):
    """From config implementation."""
    if isinstance(config, Mapping):
        # Resolve attribute, check if subclass of FromConfig
        attr = register.resolve(config[Keys.ATTR], safe=safe) if Keys.ATTR in config else None
        if attr is not None and issubclass(attr, FromConfig):
            return attr.fromconfig({key: value for key, value in config.items() if key not in Keys})

        # Resolve and instantiate args and kwargs
        args = fromconfig(config.get(Keys.ARGS, []), safe=safe)
        kwargs = {key: fromconfig(value, safe=safe) for key, value in config.items() if key not in Keys}

        # No attribute resolved, return args and kwargs
        if not attr:
            return {Keys.ARGS: args, **kwargs} if args else kwargs

        # If attribute resolved, call attribute with args and kwargs
        return attr(*args, **kwargs)

    if not isinstance(config, str) and isinstance(config, Iterable):
        # TODO: decide behavior (same type as input or list / dict)
        return type(config)(*(fromconfig(item, safe=safe) for item in config))

    return config
