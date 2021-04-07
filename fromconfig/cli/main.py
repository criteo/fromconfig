"""Main entry point."""

import functools
import sys
import logging

import fire

import fromconfig


def run(*paths: str, verbosity: int = None, **kwargs):
    """Load config, parse and instantiate.

    Parameters
    ----------
    *paths : str
        Paths to config files.
    **kwargs
        Optional key value parameters, for config, params and plugins
    """
    logging.basicConfig(level=verbosity)

    # If no paths and kwargs, return run to get fire help
    if not paths and not kwargs:
        return run

    # Expand kwargs into nested dictionary
    params = fromconfig.utils.expand(kwargs.items())

    # Load plugins
    active = params.pop("plugins", fromconfig.plugin.plugins)
    plugins = [fromconfig.plugin.plugins[name].fromconfig(params.pop(name, {})) for name in active]

    # Load configs and merge them with params from kwargs
    configs = [params] + [fromconfig.load(path) for path in paths]
    config = functools.reduce(fromconfig.utils.merge_dict, configs[::-1])

    # Parse merged config
    parser = fromconfig.parser.Chain(*[p.parser() for p in plugins if isinstance(p, fromconfig.plugin.ParserPlugin)])
    parsed = parser(config)

    # Logging
    for plugin in filter(lambda p: isinstance(p, fromconfig.plugin.LoggerPlugin), plugins):
        plugin.log(config=config, parsed=parsed)

    # Instantiate and return
    return fromconfig.fromconfig(parsed)


def main():
    """Main entry point"""
    sys.path.append(".")  # For local imports
    fire.Fire(run)
