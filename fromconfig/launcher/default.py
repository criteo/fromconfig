"""Default Launcher."""

from typing import Any

from fromconfig.core.base import FromConfig
from fromconfig.launcher import base
from fromconfig.launcher.local import LocalLauncher
from fromconfig.launcher.logger import LoggingLauncher
from fromconfig.launcher.params import ParamsLauncher
from fromconfig.launcher.parser import ParserLauncher


class DefaultLauncher(base.Launcher, FromConfig):
    """Default Launcher."""

    def __init__(self):
        self.launcher = ParamsLauncher(launcher=ParserLauncher(launcher=LoggingLauncher(launcher=LocalLauncher())))

    def __call__(self, config: Any, parsed: Any = None, command: str = ""):
        self.launcher(config=config, parsed=parsed, command=command)
