"""Local RunLauncher."""

import fire
from typing import Any
import logging

from fromconfig.launcher import base
from fromconfig.core.base import fromconfig


LOGGER = logging.getLogger(__name__)


class LocalLauncher(base.RunLauncher):
    """Local RunLauncher."""

    def run(self, parsed: Any = None, command: str = ""):
        fire.Fire(fromconfig(parsed), command)
