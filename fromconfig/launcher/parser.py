"""Parser Launcher."""

from typing import Any

from fromconfig.launcher import base
from fromconfig.parser.base import Parser
from fromconfig.parser.default import DefaultParser


class ParserLauncher(base.ParseLauncher):
    """Parser launcher."""

    def __init__(self, launcher: base.Launcher, parser: Parser = None):
        self.parser = parser or DefaultParser()
        super().__init__(launcher=launcher)

    def parse(self, config: Any):
        return self.parser(config)
