"""Logger Launcher."""

from typing import Any
import logging

from fromconfig.launcher import base
from fromconfig.utils.nest import flatten


LOGGER = logging.getLogger(__name__)


class LoggingLauncher(base.LogLauncher):
    """Logger Launcher."""

    def log(self, config: Any, command: str = "", parsed: Any = None):
        """Log parsed config params using logging module."""
        # Setup logger
        level = parsed.get("logging", {}).get("level")
        if level is not None:
            logging.basicConfig(level=level)

        # Parse config and log
        for key, value in flatten(parsed):
            LOGGER.info(f"- {key}: {value}")

        # Execute sub-launcher with no parser (already parsed)
        self.launcher(config=config, parsed=parsed, command=command)
