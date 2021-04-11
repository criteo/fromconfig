"""Main entry point."""

import functools
import sys
import logging

import fire

import fromconfig


LOGGER = logging.getLogger(__name__)


def run(paths, overrides, command):
    """Load config, parse and instantiate.

    Parameters
    ----------
    paths : str
        Paths to config files.
    overrides
        Optional key value parameters, for config, params and plugins


    1. For each config, parse + log
    2. Sweep generates new configs
    3. Launcher launch configs and get results
    4. Give results back to sweeper
    5. Repeat
    """
    # Load configs and merge them with params
    configs = [fromconfig.utils.expand(overrides.items())] + [fromconfig.load(path) for path in paths]
    config = functools.reduce(fromconfig.utils.merge_dict, configs[::-1])

    # Instantiate parser and launcher
    runconfig = config.pop("fromconfig", {})
    parser = fromconfig.fromconfig(runconfig.get("parser")) or fromconfig.parser.DefaultParser()
    launcher = fromconfig.fromconfig(runconfig.get("launcher")) or fromconfig.launcher.DefaultLauncher()

    # Launch
    launcher(parser, config, command)


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
    command = " ".join(argv[len(_paths) + len(_overrides) + 1 :])
    return _paths, _overrides, command


def main():
    """Main entry point."""
    sys.path.append(".")  # For local imports
    paths, overrides, command = parse_args()
    if paths or overrides:
        run(paths, overrides, command)
