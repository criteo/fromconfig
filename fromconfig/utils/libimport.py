"""Import utilities."""

from typing import Any
import builtins
import importlib
import inspect
import logging


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

    # If class, method or function, use __qualname__
    if inspect.isclass(attr) or inspect.ismethod(attr) or inspect.isfunction(attr):
        if module is builtins:
            return attr.__qualname__
        else:
            return f"{module.__name__}.{attr.__qualname__}"

    # Look for the instance's name in the user-defined module
    for name, member in inspect.getmembers(module):
        if id(member) == id(attr):
            return f"{module.__name__}.{name}"

    raise ValueError(f"Unable to resolve import string of {attr}")  # pragma: no cover


def from_import_string(name: str) -> Any:
    """Import module, class, method or attribute from string.

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
        raise ImportError(f"No parts found (name='{name}', parts={parts})")

    # Import modules
    module, offset = None, 0
    for idx in range(1, len(parts)):
        try:
            module_name = ".".join(parts[:idx])
            module = importlib.import_module(module_name)
            offset = idx
        except Exception as e:  # pylint: disable=broad-except
            LOGGER.info(f"Exception while loading module from {module_name}: {e}")
            break

    # Get attribute from provided module, builtins or call stack modules
    for mod in [module, builtins] + [inspect.getmodule(fi.frame) for fi in inspect.stack()]:
        try:
            attr = mod
            for part in parts[offset:]:
                attr = getattr(attr, part)
            return attr
        except Exception as e:  # pylint: disable=broad-except
            LOGGER.info(f"Exception while getting attribute from module {mod}: {e}")

    # Look for name in call stack globals
    for fi in inspect.stack():
        for key, value in fi.frame.f_globals.items():
            if key == name:
                return value

    raise ValueError(f"Unable to resolve attribute from import string '{name}'")
