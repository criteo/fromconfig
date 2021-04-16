"""Base class for launchers."""

from abc import ABC, abstractmethod
from typing import Any


class ParsedIsNotNoneError(ValueError):
    ...


class ParsedIsNoneError(ValueError):
    ...


class Launcher(ABC):
    """Base class for launchers."""

    def __call__(self, config: Any, command: str = "", parsed: Any = None):
        raise NotImplementedError()


class SweepLauncher(Launcher, ABC):
    """Base class for multi Launchers."""

    def __init__(self, launcher: Launcher):
        self.launcher = launcher

    def __call__(self, config: Any, command: str = "", parsed: Any = None):
        if parsed is not None:
            raise ParsedIsNotNoneError(parsed)
        self.sweep(config=config, command=command)

    def sweep(self, config: Any, command: str = ""):
        raise NotImplementedError()


class ParseLauncher(Launcher, ABC):
    """Base class for parse launchers."""

    def __init__(self, launcher: Launcher):
        self.launcher = launcher

    def __call__(self, config: Any, command: str = "", parsed: Any = None):
        if parsed is not None:
            raise ParsedIsNotNoneError(parsed)
        parsed = self.parse(config)
        self.launcher(config=config, parsed=parsed, command=command)

    @abstractmethod
    def parse(self, config: Any) -> Any:
        raise NotImplementedError()


class LogLauncher(Launcher, ABC):
    """Base class for log launchers."""

    def __init__(self, launcher: Launcher):
        self.launcher = launcher

    def __call__(self, config: Any, command: str = "", parsed: Any = None):
        if parsed is None:
            raise ParsedIsNoneError()
        self.log(config=config, command=command, parsed=parsed)

    @abstractmethod
    def log(self, config: Any, command: str = "", parsed: Any = None):
        raise NotImplementedError()


class RunLauncher(Launcher, ABC):
    """Base class for run launchers."""

    def __call__(self, config: Any, command: str = "", parsed: Any = None):
        if parsed is None:
            raise ParsedIsNoneError()
        self.run(parsed, command)

    @abstractmethod
    def run(self, parsed: Any, command: str = ""):
        raise NotImplementedError()
