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
        # Extract parameters
        params = config.get("logging") or {}
        level = params.get("level")
        log_config = params.get("log_config", True)

        # Change verbosity level (applies to all loggers)
        if level is not None:
            logging.basicConfig(level=level)

        # Log flattened config
        if log_config:
            for key, value in flatten(config):
                LOGGER.info(f"- {key}: {value}")

        # Execute sub-launcher with no parser (already parsed)
        self.launcher(config=config, command=command)  # type: ignore
