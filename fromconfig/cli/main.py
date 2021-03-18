"""Main entry point."""

import functools
import sys

import fire

import fromconfig


def run(*paths: str):
    """Load config, parse and instantiate.

    Parameters
    ----------
    *paths : str
        Paths to config files.
    """
    # If no paths, return run to get fire help
    if not paths:
        return run

    # Load configs and merge them
    configs = [fromconfig.load(path) for path in paths]
    config = functools.reduce(fromconfig.utils.merge_dict, configs)

    # Parse merged config
    parser = fromconfig.parser.DefaultParser()
    parsed = parser(config)

    # Instantiate and return
    return fromconfig.fromconfig(parsed)


def main():
    """Main entry point"""
    sys.path.append(".")  # For local imports
    fire.Fire(run)
