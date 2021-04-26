"""Logging Launcher."""

from typing import Any
import logging

from fromconfig.launcher import base
from fromconfig.utils.nest import flatten
from fromconfig.utils.types import is_mapping


LOGGER = logging.getLogger(__name__)


class LoggingLauncher(base.Launcher):
    """Logging Launcher."""

    def __init__(self, launcher: base.Launcher):
        super().__init__(launcher=launcher)

    def __call__(self, config: Any, command: str = ""):
        """Log parsed config params using logging module."""
        # Extract params
        params = (config.get("logging") or {}) if is_mapping(config) else {}  # type: ignore
        level = params.get("level", None)
        log_config = params.get("log_config", False)

        # Change verbosity level (applies to all loggers)
        if level is not None:
            logging.basicConfig(level=level)

        # Log flattened config
        if log_config:
            for key, value in flatten(config):
                if key in ("logging.level", "logging.log_config"):
                    continue
                LOGGER.info(f"- {key}: {value}")

        # Execute sub-launcher with no parser (already parsed)
        self.launcher(config=config, command=command)  # type: ignore
