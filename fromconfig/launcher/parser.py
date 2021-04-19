"""Parse the config."""

from typing import Any
import logging

from fromconfig.core.base import fromconfig
from fromconfig.launcher import base
from fromconfig.parser.default import DefaultParser
from fromconfig.parser.singleton import singleton


LOGGER = logging.getLogger(__name__)


class ParserLauncher(base.Launcher):
    """Parse the config."""

    def __call__(self, config: Any, command: str = ""):
        parser = fromconfig(config.pop("parser")) if "parser" in config else DefaultParser()
        LOGGER.info(f"Resolved parser {parser}")
        self.launcher(config=parser(config), command=command)  # type: ignore
        singleton.clear()  # Clear singleton to avoid leaks
