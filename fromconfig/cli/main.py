"""Main entry point."""

import sys

import fire

import fromconfig


def run(path: str, safe: bool = False):
    """Load config, parse and instantiate.

    Parameters
    ----------
    path : str
        Path to config file
    safe : bool, optional
        If True, use safe mode to resolve modules and attributes.
    """
    parser = fromconfig.parser.DefaultParser()
    parsed = parser(fromconfig.load(path))
    return fromconfig.fromconfig(parsed, safe=safe)


def main():
    """Main entry point"""
    sys.path.append(".")
    fire.Fire({"run": run})


if __name__ == "__main__":
    main()
