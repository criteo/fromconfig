"""Base class for plugins."""

from abc import ABC
from typing import Any

from fromconfig.parser.base import Parser


class Plugin(ABC):
    """Base Plugin Class."""


class ParserPlugin(Plugin, ABC):
    """Base class for parser plugins."""

    def parser(self, parser: Parser) -> Parser:
        """Create parser from existing parser.

        Parameters
        ----------
        parser : fromconfig.parser.Parser
            Parser from previous plugins or DefaultParser

        Returns
        -------
        fromconfig.parser.Parser
        """
        return parser


class LoggingPlugin(Plugin, ABC):
    """Base class for logging plugins."""

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
