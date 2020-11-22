"""Command line interface."""

import sys
import os
import logging

import fire
from fireconfig import core
from fireconfig import io


LOGGER = logging.getLogger(__name__)


def run(config):
    config = core.parse_config(io.read(config))
    return core.from_config(config["main"])


def from_config(config):
    config = core.parse_config(io.read(config))
    return core.from_config(config)


def main():
    """Main entry point"""
    sys.path.append(os.getcwd())
    logging.basicConfig(level=logging.INFO)
    fire.Fire({"run": run, "from_config": from_config})


if __name__ == "__main__":
    main()
