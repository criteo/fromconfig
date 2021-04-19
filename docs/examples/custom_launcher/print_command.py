"""Custom Launcher that prints the command."""

from typing import Any

import fromconfig


class PrintCommandLauncher(fromconfig.launcher.Launcher):
    def __call__(self, config: Any, command: str = ""):
        print(command)
