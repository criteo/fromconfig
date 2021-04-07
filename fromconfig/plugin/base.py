"""Base class for plugins."""

from abc import ABC
import pkg_resources
import logging
import collections

from fromconfig.core.base import FromConfig
from fromconfig.version import MAJOR


LOGGER = logging.getLogger(__name__)


class Plugin(FromConfig, ABC):
    """Base Plugin Class."""


class PluginRegistry(collections.UserDict):
    """Plugins Registry.

    TODO: resolve lazy loading / cyclic import issue
    """

    def __setitem__(self, key, value):
        if key in self and value is not self[key]:
            raise KeyError(f"Plugin name conflict for name {key} ({value} and {self[key]})")
        super().__setitem__(key, value)

    def register(self, name: str):
        """Return register decorator to add plugin to registry."""

        def _register(plugin):
            self[name] = plugin

        return _register

    def _load(self):
        for entry_point in pkg_resources.iter_entry_points(f"fromconfig{MAJOR}"):
            self[entry_point.name] = entry_point.load()
            try:
                self[entry_point.name] = entry_point.load()
            except Exception as e:  # pylint: disable=broad-except
                LOGGER.error(f"Exception while loading plugin {entry_point.name} ({e})")


plugins = PluginRegistry()
