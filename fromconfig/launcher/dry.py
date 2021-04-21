"""Dry Launcher."""

from typing import Any
import logging
from pprint import pprint

from fromconfig.launcher import base


LOGGER = logging.getLogger(__name__)


class DryLauncher(base.Launcher):
    """Dry Launcher."""

    def __init__(self, launcher: base.Launcher = None):
        super().__init__(launcher=launcher)  # type: ignore

    def __call__(self, config: Any, command: str = ""):
        pprint(config)
        print(command)
