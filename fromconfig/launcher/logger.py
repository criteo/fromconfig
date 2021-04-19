"""Logging Launcher."""

from typing import Any
import logging

from fromconfig.launcher import base
from fromconfig.utils.nest import flatten


LOGGER = logging.getLogger(__name__)


class LoggingLauncher(base.Launcher):
    """Logging Launcher."""

    def __call__(self, config: Any, command: str = ""):
        """Log parsed config params using logging module."""
        # Setup logger
        level = config.get("logging", {}).get("level")
        if level is not None:
            logging.basicConfig(level=level)

        # Parse config and log
        for key, value in flatten(config):
            LOGGER.info(f"- {key}: {value}")

        # Execute sub-launcher with no parser (already parsed)
        self.launcher(config=config, command=command)  # type: ignore
