"""Hyper Params SweepLauncher."""

from typing import Any
import itertools
import logging

from fromconfig.core.base import fromconfig
from fromconfig.launcher import base
from fromconfig.utils.nest import merge_dict


LOGGER = logging.getLogger(__name__)


class HParamsLauncher(base.Launcher):
    """Hyper Params Launcher.

    Given a config, it extracts hyper parameters ranges by instantiating
    the `hparams` entry of the config.

    It then generates sets of parameters and merge their values into
    the `hparams` entry of the config.

    Attributes
    ----------
    launcher : Launcher
        Launcher to launch each sub-job
    """

    def __call__(self, config: Any, command: str = ""):
        """Generate configs via hyper-parameters."""
        hparams = fromconfig(config.get("hparams", {}))
        if not hparams:
            self.launcher(config=config, command=command)
        else:
            names = hparams.keys()
            for values in itertools.product(*[hparams[name] for name in names]):
                overrides = dict(zip(names, values))
                LOGGER.info("Launching with params")
                for key, value in overrides.items():
                    LOGGER.info(f"- {key}: {value}")
                self.launcher(config=merge_dict(config, {"hparams": overrides}), command=command)
