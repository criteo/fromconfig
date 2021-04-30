"""Hyper Params SweepLauncher."""

from typing import Any
import itertools
import logging
import shutil

from fromconfig.core.base import fromconfig
from fromconfig.launcher import base
from fromconfig.utils.nest import merge_dict
from fromconfig.utils.types import is_mapping


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
        if not is_mapping(config):
            self.launcher(config=config, command=command)
        else:
            hparams = fromconfig(config.get("hparams") or {})
            if not hparams:
                self.launcher(config=config, command=command)
            else:
                names = hparams.keys()
                for values in itertools.product(*[hparams[name] for name in names]):
                    overrides = dict(zip(names, values))
                    print(header(overrides))
                    self.launcher(config=merge_dict(config, {"hparams": overrides}), command=command)


def header(overrides) -> str:
    """Create header for experiment."""
    # Get terminal number of columns
    try:
        columns, _ = shutil.get_terminal_size((80, 20))
    except Exception:  # pylint: disable=broad-except
        columns = 80

    # Join key-values and truncate if needed
    content = ", ".join(f"{key}={value}" for key, value in overrides.items())
    if len(content) >= columns - 2:
        content = content[: columns - 2 - 3] + "." * 3
    content = f"[{content}]"

    # Add padding
    padding = "=" * max((columns - len(content)) // 2, 0)
    return f"{padding}{content}{padding}"
