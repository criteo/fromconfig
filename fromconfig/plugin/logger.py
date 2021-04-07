"""Base class for Logger Plugins."""

from abc import ABC, abstractmethod
import logging
from typing import Any

from fromconfig.plugin import base
from fromconfig.utils.nest import flatten


LOGGER = logging.getLogger(__name__)


class LoggerPlugin(base.Plugin, ABC):
    """Base class for logging plugins."""

    @abstractmethod
    def log(self, config: Any, parsed: Any):
        """Log config during run call.

        Parameters
        ----------
        config : Any
            Result of the reduction of different config files.
        parsed : Any
            Result of the config parsing.
        """
        pass


@base.plugins.register("logger")
class DefaultLoggerPlugin(LoggerPlugin):
    """Default Logger Plugin."""

    def log(self, config: Any, parsed: Any):
        for key, value in flatten(parsed):
            LOGGER.info(f"{key}: {value}")
