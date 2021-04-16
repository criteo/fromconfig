"""ParseLauncher using the DefaultParser."""

from typing import Any

from fromconfig.launcher import base
from fromconfig.parser.base import Parser
from fromconfig.parser.default import DefaultParser
from fromconfig.parser.singleton import singleton


class ParserLauncher(base.ParseLauncher):
    """ParseLauncher using the DefaultParser."""

    def __init__(self, launcher: base.Launcher, parser: Parser = None):
        self.parser = parser or DefaultParser()
        super().__init__(launcher=launcher)

    def parse(self, config: Any):
        return self.parser(config)

    def teardown(self):
        # The SingletonParser uses singleton to store singletons
        # during instantiation. Clear it to avoid leaks between
        # different consecutive launchers (during a parameter sweep).
        singleton.clear()
