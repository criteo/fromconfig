"""Base class for launchers."""

from abc import ABC, abstractmethod
from typing import Any


class ParsedIsNotNoneError(ValueError):
    """Parsed is not None, but config should not be parsed yet."""


class ParsedIsNoneError(ValueError):
    """Parsed is None, but config should already be parsed."""


class Launcher(ABC):
    """Base class for launchers."""

    def __call__(self, config: Any, command: str = "", parsed: Any = None):
        """Launch implementation.

        Parameters
        ----------
        config : Any
            The unparsed config
        command : str, optional
            The fire command
        parsed : Any, optional
            The parsed config, if any
        """
        self.setup()
        self.launch(config=config, command=command, parsed=parsed)
        self.teardown()

    def setup(self):
        """Optional setup step."""

    @abstractmethod
    def launch(self, config: Any, command: str = "", parsed: Any = None):
        """Subclasses must implement."""
        raise NotImplementedError()

    def teardown(self):
        """Optional teardown step."""


class SweepLauncher(Launcher, ABC):
    """Base class for sweep launchers."""

    def __init__(self, launcher: Launcher):
        self.launcher = launcher

    def setup(self):
        self.launcher.setup()

    def launch(self, config: Any, command: str = "", parsed: Any = None):
        if parsed is not None:
            raise ParsedIsNotNoneError(parsed)
        self.sweep(config=config, command=command)

    @abstractmethod
    def sweep(self, config: Any, command: str = ""):
        """Launch multiple launchers on different configs.

        Parameters
        ----------
        config : Any
            The unparsed config
        command : str, optional
            The fire command
        """
        raise NotImplementedError()

    def teardown(self):
        self.launcher.teardown()


class ParseLauncher(Launcher, ABC):
    """Base class for parse launchers."""

    def __init__(self, launcher: Launcher):
        self.launcher = launcher

    def setup(self):
        self.launcher.setup()

    def launch(self, config: Any, command: str = "", parsed: Any = None):
        if parsed is not None:
            raise ParsedIsNotNoneError(parsed)
        parsed = self.parse(config)
        self.launcher(config=config, parsed=parsed, command=command)

    @abstractmethod
    def parse(self, config: Any) -> Any:
        """Subclasses must implement."""
        raise NotImplementedError()

    def teardown(self):
        self.launcher.teardown()


class LogLauncher(Launcher, ABC):
    """Base class for log launchers."""

    def __init__(self, launcher: Launcher):
        self.launcher = launcher

    def setup(self):
        self.launcher.setup()

    def launch(self, config: Any, command: str = "", parsed: Any = None):
        if parsed is None:
            raise ParsedIsNoneError()
        self.log(config=config, command=command, parsed=parsed)

    @abstractmethod
    def log(self, config: Any, command: str = "", parsed: Any = None):
        """Subclasses must implement."""
        raise NotImplementedError()

    def teardown(self):
        self.launcher.teardown()


class RunLauncher(Launcher, ABC):
    """Base class for run launchers."""

    def launch(self, config: Any, command: str = "", parsed: Any = None):
        if parsed is None:
            raise ParsedIsNoneError()
        self.run(parsed, command)

    @abstractmethod
    def run(self, parsed: Any, command: str = ""):
        """Subclasses must implement."""
        raise NotImplementedError()
