"""Import utilities."""

from typing import Any
import importlib
import builtins
import logging
import inspect


LOGGER = logging.getLogger(__name__)


def try_import(name, package=None):
    """Try import package name in package."""
    try:
        return importlib.import_module(name, package=package)
    except ImportError as e:
        LOGGER.error(f"Unable to import {name}, {e}")
        return None


def to_import_string(attr: Any) -> str:
    """Retrieve import string from attribute.

    Parameters
    ----------
    attr : Any
        Any python function, class or method
    """
    if inspect.ismodule(attr):
        return attr.__name__
    module = inspect.getmodule(attr)
    if module is None:
        raise ValueError(f"Unable to resolve module of {attr}")
    if inspect.isclass(attr) or inspect.ismethod(attr) or inspect.isfunction(attr):
        if module is builtins:
            return attr.__qualname__
        else:
            return f"{module.__name__}.{attr.__qualname__}"
    if not hasattr(attr, "__class__"):
        raise ValueError(f"Unable to resolve class of {attr}")
    return to_import_string(attr.__class__)


def from_import_string(name: str) -> Any:
    """Import from string.

    Examples
    --------
    >>> import fromconfig
    >>> fromconfig.utils.from_import_string("str") == str
    True

    Parameters
    ----------
    name : str
        Import string or builtin name
    """
    # Resolve import parts
    parts = [part for part in name.split(".") if part]
    if not parts:
        raise ImportError(f"No module specified ({name})")

    # Import modules
    module, part = None, 0
    for idx in range(1, len(parts)):
        try:
            module_name = ".".join(parts[:idx])
            module = importlib.import_module(module_name)
            part = idx
        except Exception as e:  # pylint: disable=broad-except
            LOGGER.info(f"Exception while loading module from {module_name}: {e}")
            break

    # Resolve attribute
    attr = module if module is not None else builtins
    for part_name in parts[part:]:
        attr = getattr(attr, part_name)

    return attr
