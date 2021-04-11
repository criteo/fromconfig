"""Default Launcher."""

from typing import Dict, List, Any

from fromconfig.parser.base import Parser
from fromconfig.launcher import base
from fromconfig.launcher.local import LocalLauncher
from fromconfig.launcher.logger import LoggerLauncher
from fromconfig.launcher.multi import MultiLauncher


class DefaultLauncher(base.Launcher):
    """Default Launcher."""

    def __init__(self, params: Dict[str, List[Any]] = None, level: int = None):
        self.launcher = MultiLauncher(
            launcher=LoggerLauncher(
                launcher=LocalLauncher(),
                level=level
                ),
            params=params
            )

    def __call__(self, parser: Parser, config: Any, command: str):
        self.launcher(parser=parser, config=config, command=command)
