"""Logger Launcher."""

from typing import Any
import logging

from fromconfig.parser.base import Parser, ChainParser
from fromconfig.launcher.local import LocalLauncher
from fromconfig.launcher import base
from fromconfig.utils.nest import flatten


LOGGER = logging.getLogger(__name__)


class LoggerLauncher(base.Launcher):
    """Logger Launcher."""

    def __init__(self, launcher: base.Launcher = None, level: int = None):
        self.launcher = launcher or LocalLauncher()
        self.level = level
        if self.level is not None:
            logging.basicConfig(level=self.level)

    def __call__(self, parser: Parser, config: Any, command: str):
        # Parse config and log
        parsed = parser(config)
        for key, value in flatten(parsed):
            LOGGER.info(f"- {key}: {value}")

        # Execute sub-launcher with no parser (already parsed)
        self.launcher(parser=ChainParser(), config=parsed, command=command)
