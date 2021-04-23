"""Convert file format."""

import fire

import fromconfig


def convert(path_input, path_output):
    """Convert input into output with load and dump."""
    fromconfig.dump(fromconfig.load(path_input), path_output)


if __name__ == "__main__":
    fire.Fire(convert)
