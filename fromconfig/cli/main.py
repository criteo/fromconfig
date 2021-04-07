"""Main entry point."""

import functools
import sys
import logging

import fire

import fromconfig


def run(*paths: str, **kwargs):
    """Load config, parse and instantiate.

    Parameters
    ----------
    *paths : str
        Paths to config files.
    **kwargs
        Optional key value parameters, for config, params and plugins
    """
    # If no paths and kwargs, return run to get fire help
    if not paths and not kwargs:
        return run

    # Expand kwargs into nested dictionary
    params = fromconfig.utils.expand(kwargs.items())

    # Extract parameters
    allow_override = params.pop("allow_override", True)
    level = params.pop("logging", {}).get("level", logging.INFO)

    # Load plugins
    plugins = [
        fromconfig.plugin.plugins()[name](**params.pop(name, {}))
        for name in params.pop("plugins", fromconfig.plugin.plugins())
    ]

    # Set verbosity level
    logging.basicConfig(level=level)

    # Load configs and merge them with params from kwargs
    configs = [params] + [fromconfig.load(path) for path in paths]
    config = functools.reduce(
        functools.partial(fromconfig.utils.merge_dict, allow_override=allow_override), configs[::-1]
    )

    # Resolve parser
    parser = fromconfig.parser.DefaultParser()
    for plugin in filter(lambda p: isinstance(p, fromconfig.plugin.ParserPlugin), plugins):
        parser = plugin.parser(parser)

    # Parse merged config
    parsed = parser(config)

    # Logging
    for plugin in filter(lambda p: isinstance(p, fromconfig.plugin.LoggingPlugin), plugins):
        plugin.log(config=config, parsed=parsed)

    # Instantiate and return
    return fromconfig.fromconfig(parsed)


def main():
    """Main entry point"""
    sys.path.append(".")  # For local imports
    fire.Fire(run)
