"""Base functionality."""

from abc import ABC, abstractclassmethod
import inspect
import logging
from typing import Any, Mapping

from fromconfig.core.register import register
from fromconfig.utils import StrEnum, is_iterable, is_mapping, try_init


LOGGER = logging.getLogger(__name__)


class Keys(StrEnum):
    """Special Keys."""

    ATTR = "_attr_"
    ARGS = "_args_"


class FromConfig(ABC):
    """Abstract class for custom from_config implementations."""

    @abstractclassmethod
    def fromconfig(cls, config: Mapping):
        """Subclasses must override.

        Parameters
        ----------
        config : Mapping
            Config dictionary, non-instantiated.
        """
        raise NotImplementedError()


def fromconfig(config: Any, safe: bool = False):
    """From config implementation.

    Examples
    --------
    >>> import fromconfig
    >>> @fromconfig.register("Model")
    ... class Model:
    ...     def __init__(self, dim):
    ...         self.dim = dim
    >>> config = {"_attr_": "Model", "dim": 100}
    >>> model = fromconfig.fromconfig(config)
    >>> isinstance(model, Model)
    True
    >>> model.dim
    100

    Parameters
    ----------
    config : Any
        Typically a dictionary
    safe : bool, optional
        If True, don't use import string to resolve attributes.
    """
    if is_mapping(config):
        # Resolve attribute, check if subclass of FromConfig
        attr = register.resolve(config[Keys.ATTR], safe=safe) if Keys.ATTR in config else None
        if inspect.isclass(attr) and issubclass(attr, FromConfig):
            return attr.fromconfig({key: value for key, value in config.items() if key != Keys.ATTR})

        # Resolve and instantiate args and kwargs
        args = fromconfig(config.get(Keys.ARGS, []), safe=safe)
        kwargs = {key: fromconfig(value, safe=safe) for key, value in config.items() if key not in Keys}

        # No attribute resolved, return args and kwargs
        if attr is None:
            kwargs = {Keys.ARGS: args, **kwargs} if args else kwargs
            return try_init(type(config), dict, kwargs)

        # If attribute resolved, call attribute with args and kwargs
        return attr(*args, **kwargs)

    if is_iterable(config):
        args = [fromconfig(item, safe=safe) for item in config]
        return try_init(type(config), list, args)

    return config
