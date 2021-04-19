"""Default Launcher."""

from typing import Any

from fromconfig.launcher import base
from fromconfig.launcher.hparams import HParamsLauncher
from fromconfig.launcher.local import LocalLauncher
from fromconfig.launcher.logger import LoggingLauncher
from fromconfig.launcher.parser import ParserLauncher


class DefaultLauncher(base.Launcher):
    """Default Launcher.

    Attributes
    ----------
    launcher : Launcher
        The wrapped launcher.
    """

    def __init__(self, launcher: base.Launcher = None):
        super().__init__(launcher or HParamsLauncher(ParserLauncher(LoggingLauncher(LocalLauncher()))))

    def __call__(self, config: Any, command: str = ""):
        self.launcher(config=config, command=command)
