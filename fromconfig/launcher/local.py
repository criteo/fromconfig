"""Local Launcher."""

from typing import Any
import fire
import logging

from fromconfig.core.base import fromconfig
from fromconfig.launcher import base


LOGGER = logging.getLogger(__name__)


class LocalLauncher(base.Launcher):
    """Local Launcher."""

    def __init__(self, launcher: base.Launcher = None):
        if launcher is not None:
            raise ValueError(f"LocalLauncher cannot wrap another launcher but got {launcher}")
        super().__init__(launcher=launcher)  # type: ignore

    def __call__(self, config: Any, command: str = ""):
        fire.Fire(fromconfig(config), command)
