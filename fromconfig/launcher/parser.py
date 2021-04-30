"""Parse the config."""

from typing import Any
import logging

from fromconfig.core.base import fromconfig
from fromconfig.launcher import base
from fromconfig.parser.default import DefaultParser
from fromconfig.parser.singleton import singleton
from fromconfig.utils.types import is_mapping


LOGGER = logging.getLogger(__name__)


class ParserLauncher(base.Launcher):
    """Parse the config."""

    def __call__(self, config: Any, command: str = ""):
        # Resolve parser
        if is_mapping(config):
            parser = fromconfig(config.pop("parser")) if "parser" in config else DefaultParser()
        else:
            parser = DefaultParser()
        LOGGER.debug(f"Resolved parser {parser}")

        # Launch
        self.launcher(config=parser(config) if callable(parser) else config, command=command)  # type: ignore

        # Clear singleton to avoid leaks
        singleton.clear()
