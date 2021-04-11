"""Local Launcher."""

import fire
from typing import Any

from fromconfig.launcher import base
from fromconfig.parser.base import Parser
from fromconfig.core.base import fromconfig


class LocalLauncher(base.Launcher):
    """Local Launcher."""

    def __call__(self, parser: Parser, config: Any, command: str):
        return fire.Fire(fromconfig(parser(config)), command)
