"""Local Launcher."""

import fire
from typing import Any
import logging

from fromconfig.launcher import base
from fromconfig.core.base import fromconfig


LOGGER = logging.getLogger(__name__)


class LocalLauncher(base.Launcher):
    """Local Launcher."""

    def __init__(self, launcher: base.Launcher = None):
        if launcher is not None:
            raise ValueError(f"LocalLauncher cannot wrap another launcher but got {launcher}")
        super().__init__(launcher=launcher)

    def __call__(self, config: Any, command: str = ""):
        fire.Fire(fromconfig(config), command)
