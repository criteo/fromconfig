"""Multi."""

import itertools
from typing import Dict, List, Any
import logging

from fromconfig.parser.base import Parser
from fromconfig.launcher.local import LocalLauncher
from fromconfig.launcher import base
from fromconfig.utils.nest import merge_dict


LOGGER = logging.getLogger(__name__)


class MultiLauncher(base.Launcher):
    """Multi Launcher."""

    def __init__(self, launcher: base.Launcher = None, params: Dict[str, List[Any]] = None):
        self.launcher = launcher or LocalLauncher()
        self.params = params

    def __call__(self, parser: Parser, config: Any, command: str):
        if not self.params:
            self.launcher(parser=parser, config=config, command=command)
        else:
            names = self.params.keys()
            for values in itertools.product(*[self.params[name] for name in names]):
                overrides = dict(zip(names, values))
                LOGGER.info("Launching with params")
                for key, value in overrides.items():
                    LOGGER.info(f"- {key}: {value}")
                self.launcher(parser=parser, config=merge_dict(config, {"params": overrides}), command=command)
