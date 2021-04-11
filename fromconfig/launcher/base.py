"""Base class for launchers."""

from abc import ABC


class Launcher(ABC):
    """Base class for launchers."""

    def __call__(self, config, command):
        raise NotImplementedError()
