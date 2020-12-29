"""Import utilities."""

from typing import Any
import importlib
import builtins
import logging


LOGGER = logging.getLogger(__name__)


def import_from_string(name: str) -> Any:
    """Import from string.

    Examples
    --------
    >>> import fromconfig
    >>> fromconfig.utils.import_from_string("str") == str
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
    for part in range(1, len(parts) - 1):
        try:
            name = ".".join(parts[:part])
            module = importlib.import_module(name)
        except Exception as e:  # pylint: disable=broad-except
            LOGGER.info(f"Exception while loading module from {name}: {e}")
            break

    # Resolve attribute
    attr = module if module is not None else builtins
    for part in parts[part:]:
        attr = getattr(attr, part)

    return attr
