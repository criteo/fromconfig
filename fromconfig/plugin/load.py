"""Discover plugins."""

import pkg_resources
import logging
from typing import Dict

from fromconfig.version import MAJOR
from fromconfig.plugin import base


LOGGER = logging.getLogger(__name__)


_PLUGINS: Dict[str, base.Plugin] = {}
_LOADED = False


def load():
    for entry_point in pkg_resources.iter_entry_points(f"fromconfig{MAJOR}"):
        plugin = entry_point.load()
        if not issubclass(plugin, base.Plugin):
            LOGGER.warning(f"Invalid plugin {plugin}. Expected class Plugin, got {plugin}.")
        _PLUGINS[entry_point.name] = plugin


def plugins():
    """Return plugins."""
    if not _LOADED:
        load()
    return dict(_PLUGINS)  # Shallow copy to avoid overrides
