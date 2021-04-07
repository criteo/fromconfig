"""Base class for Parser Plugins."""

from abc import ABC, abstractmethod

from fromconfig.plugin import base
from fromconfig.parser.base import Parser
from fromconfig.parser.default import DefaultParser


class ParserPlugin(base.Plugin, ABC):
    """Base class for parser plugins."""

    @abstractmethod
    def parser(self) -> Parser:
        """Create parser to be chained with other active parsers.

        Returns
        -------
        Parser
        """
        raise NotImplementedError()


@base.plugins.register("parser")
class DefaultParserPlugin(ParserPlugin):
    """Default Parser Plugin."""

    def parser(self) -> Parser:
        return DefaultParser()
