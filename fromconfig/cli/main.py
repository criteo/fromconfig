"""Main entry point."""

import functools
import sys
import logging
from typing import Iterable, Mapping

import fire

import fromconfig


LOGGER = logging.getLogger(__name__)


def launch(paths: Iterable[str], overrides: Mapping, command: str):
    """Load configs, merge, get launcher from plugins and launch.

    Parameters
    ----------
    paths : Iterable[str]
        Paths to config files.
    overrides : Mapping
        Optional key value parameters that overrides config files
    command : str
        Rest of the python Fire command
    """
    configs = [fromconfig.load(path) for path in paths] + [fromconfig.utils.expand(overrides.items())]
    config = functools.reduce(fromconfig.utils.merge_dict, configs)
    launcher = fromconfig.launcher.DefaultLauncher.fromconfig(config.pop("launcher", {}))
    launcher(config=config, command=command)


def parse_args():
    """Parse arguments from command line using Fire."""
    _paths, _overrides = [], {}  # pylint: disable=invalid-name

    def _parse_args(*paths, **overrides):
        # Display Fire Help
        if not paths and not overrides:
            return _parse_args

        # Extract paths and overrides from arguments
        _paths.extend(paths)
        _overrides.update(overrides)

        # Do nothing with remaining arguments
        def _no_op(*_args, **_kwargs):
            return None if not (_args or _kwargs) else _no_op

        return _no_op

    argv = sys.argv[1:]
    fire.Fire(_parse_args, argv)
    num_args_used = len(_paths) + len(_overrides) + 1  # +1 for the fire separator
    command = " ".join(argv[num_args_used:])
    return _paths, _overrides, command


def main():
    """Main entry point."""
    sys.path.append(".")  # For local imports
    paths, overrides, command = parse_args()
    if paths or overrides:
        launch(paths, overrides, command)
