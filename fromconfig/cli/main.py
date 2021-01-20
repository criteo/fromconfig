"""Main entry point."""

import sys

import fire

import fromconfig


def run(*path_configs: str, safe: bool = False, path_parser: str = None):
    """Load configs, parse and instantiate.

    Parameters
    ----------
    *configs : str
        List of paths to config files
    """
    # Load configs and merge
    configs = [fromconfig.load(path) for path in path_configs]
    merged = {}  # type: ignore
    for idx, config in enumerate(configs):
        if not fromconfig.utils.is_mapping(config):
            raise TypeError(f"Expected type Mapping but got {type(config)} from path {path_configs[idx]}")
        merged = fromconfig.utils.merge_dict(merged, config)  # type: ignore

    # Parse and return
    parser = fromconfig.fromconfig(fromconfig.load(path_parser)) if path_parser else fromconfig.parser.DEFAULT
    parsed = fromconfig.parser.parse(merged, parser=parser)
    return fromconfig.fromconfig(parsed, safe)


def main():
    """Main entry point"""
    sys.path.append(".")
    fire.Fire({"run": run})


if __name__ == "__main__":
    main()
