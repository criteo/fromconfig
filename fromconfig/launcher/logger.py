"""Logging Launcher."""

from typing import Any
import logging

from fromconfig.launcher import base
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

        # Change verbosity level (applies to all loggers)
        if level is not None:
            logging.basicConfig(level=level)

        # Execute sub-launcher with no parser (already parsed)
        self.launcher(config=config, command=command)  # type: ignore
