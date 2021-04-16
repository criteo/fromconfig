"""Main entry point."""

import functools
import sys
import logging
from typing import Iterable, Mapping

import fire

import fromconfig
from fromconfig.cli.plugins import Plugins


LOGGER = logging.getLogger(__name__)


def run(paths: Iterable[str], overrides: Mapping, command: str):
    """Load config, parse and instantiate.

    Parameters
    ----------
    paths : Iterable[str]
        Paths to config files.
    overrides : Mapping
        Optional key value parameters that overrides config files
    command : str
        Rest of the python Fire command
    """
    # Load configs and merge them with params
    configs = [fromconfig.utils.expand(overrides.items())] + [fromconfig.load(path) for path in paths]
    config = functools.reduce(fromconfig.utils.merge_dict, configs[::-1])
    plugins = Plugins.fromconfig(config.get("fromconfig", {}))
    plugins.launcher(config=config, command=command)


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
    num_args_used = len(_paths) + len(_overrides)
    command = " ".join(argv[(num_args_used + 1) :])
    return _paths, _overrides, command


def main():
    """Main entry point."""
    sys.path.append(".")  # For local imports
    paths, overrides, command = parse_args()
    if paths or overrides:
        run(paths, overrides, command)
