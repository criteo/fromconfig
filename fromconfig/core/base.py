"""Base functionality."""

from abc import ABC, abstractclassmethod
import logging

from fromconfig.utils import StrEnum, is_iterable, is_mapping, try_init
from fromconfig.core.register import register


LOGGER = logging.getLogger(__name__)


class Keys(StrEnum):
    """Special Keys."""

    ATTR = "_attr_"
    ARGS = "_args_"


class FromConfig(ABC):
    """Abstract class for custom from_config implementations."""

    @abstractclassmethod
    def fromconfig(cls, config):
        raise NotImplementedError()


def fromconfig(config, safe: bool = False):
    """From config implementation."""
    if is_mapping(config):
        # Resolve attribute, check if subclass of FromConfig
        attr = register.resolve(config[Keys.ATTR], safe=safe) if Keys.ATTR in config else None
        if attr is not None and issubclass(attr, FromConfig):
            return attr.fromconfig({key: value for key, value in config.items() if key != Keys.ATTR})

        # Resolve and instantiate args and kwargs
        args = fromconfig(config.get(Keys.ARGS, []), safe=safe)
        kwargs = {key: fromconfig(value, safe=safe) for key, value in config.items() if key not in Keys}

        # No attribute resolved, return args and kwargs
        if not attr:
            kwargs = {Keys.ARGS: args, **kwargs} if args else kwargs
            return try_init(type(config), dict, kwargs)

        # If attribute resolved, call attribute with args and kwargs
        return attr(*args, **kwargs)

    if is_iterable(config):
        args = [fromconfig(item, safe=safe) for item in config]
        return try_init(type(config), list, args)

    return config
