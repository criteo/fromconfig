"""Base functionality."""

from abc import ABC
from typing import Any, Mapping
import inspect
import logging

from fromconfig.utils import StrEnum, is_pure_iterable, is_mapping, from_import_string


LOGGER = logging.getLogger(__name__)


class Keys(StrEnum):
    """Special Keys used by fromconfig.

    Attributes
    ----------
    ARGS : str
        Name of the special key for the full import string.
    ATTR : str
        Name of the special key for positional arguments.
    """

    ATTR = "_attr_"
    ARGS = "_args_"


class FromConfig(ABC):
    """Abstract class for custom from_config implementations.

    Example
    -------
    >>> import fromconfig
    >>> class MyClass(fromconfig.FromConfig):
    ...     def __init__(self, x):
    ...         self.x = x
    ...     @classmethod
    ...     def fromconfig(cls, config):
    ...         if "x" not in config:
    ...             return cls(0)
    ...         else:
    ...             return cls(**config)
    >>> config = {}
    >>> got = MyClass.fromconfig(config)
    >>> isinstance(got, MyClass)
    True
    >>> got.x
    0
    """

    @classmethod
    def fromconfig(cls, config: Mapping):
        """Subclasses must override.

        Parameters
        ----------
        config : Mapping
            Config dictionary, non-instantiated.
        """
        args = fromconfig(config.get(Keys.ARGS, []))
        kwargs = {key: fromconfig(value) for key, value in config.items() if key not in Keys}
        return cls(*args, **kwargs)  # type: ignore


def fromconfig(config: Any):
    """From config implementation.

    Example
    -------
    Use the '_attr_' key to configure the class, function, variable or
    method to configure. It is generally the full import string or the
    name of the class for builtins.

    >>> import fromconfig
    >>> config = {"_attr_": "str", "_args_": [1]}
    >>> fromconfig.fromconfig(config)
    '1'

    A more complicated example is
    >>> import fromconfig
    >>> class Point:
    ...     def __init__(self, x, y):
    ...         self.x = x
    ...         self.y = y
    >>> config = {
    ...     "_attr_": "Point",
    ...     "x": 0,
    ...     "y": 0
    ... }
    >>> point = fromconfig.fromconfig(config)
    >>> isinstance(point, Point) and point.x == 0 and point.y == 0
    True

    Parameters
    ----------
    config : Any
        Typically a dictionary
    """
    if is_mapping(config):
        # Resolve attribute, check if subclass of FromConfig
        attr = from_import_string(config[Keys.ATTR]) if Keys.ATTR in config else None
        if inspect.isclass(attr) and issubclass(attr, FromConfig):
            return attr.fromconfig({key: value for key, value in config.items() if key != Keys.ATTR})

        # Resolve and instantiate args and kwargs
        args = fromconfig(config.get(Keys.ARGS, []))
        kwargs = {key: fromconfig(value) for key, value in config.items() if key not in Keys}

        # No attribute resolved, return args and kwargs
        if attr is None:
            return type(config)({Keys.ARGS: args, **kwargs}) if args else type(config)(kwargs)

        # If attribute resolved, call attribute with args and kwargs
        return attr(*args, **kwargs)

    if is_pure_iterable(config):
        return type(config)(fromconfig(item) for item in config)

    return config
