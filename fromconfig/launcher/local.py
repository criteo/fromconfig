"""Local Run Launcher."""

import fire
from typing import Any

from fromconfig.launcher import base
from fromconfig.core.base import fromconfig


class LocalLauncher(base.RunLauncher):
    """Local Run Launcher."""

    def run(self, parsed: Any = None, command: str = ""):
        return fire.Fire(fromconfig(parsed), command)
