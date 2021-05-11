"""Default Launcher."""

from collections import OrderedDict
from typing import Any

from fromconfig.launcher import base
from fromconfig.launcher.hparams import HParamsLauncher
from fromconfig.launcher.local import LocalLauncher
from fromconfig.launcher.logger import LoggingLauncher
from fromconfig.launcher.parser import ParserLauncher
from fromconfig.utils.types import is_mapping


# Special keys for a Launcher config split by steps with defaults
_STEPS = OrderedDict(
    [
        ("sweep", "hparams"),  # Hyper Parameter Sweep
        ("log", "logging"),  # Configure Logging
        ("parse", "parser"),  # Parse config
        ("run", "local"),  # Actually run the config
    ]
)


class DefaultLauncher(base.Launcher):
    """Default Launcher.

    Attributes
    ----------
    launcher : Launcher
        The wrapped launcher.
    """

    def __init__(self, launcher: base.Launcher = None):
        super().__init__(launcher or HParamsLauncher(LoggingLauncher(ParserLauncher(LocalLauncher()))))

    def __call__(self, config: Any, command: str = ""):
        self.launcher(config=config, command=command)

    @classmethod
    def fromconfig(cls, config):
        """Custom fromconfig implementation.

        The config can be a dictionary with special keys run, log, parse
        and sweep. Each of these values can either be a plain dictionary
        or a Launcher class name. In that case, it is equivalent to a
        list of launchers defined in the sweep -> parse -> log -> run
        order. When overriding only a subset of these keys, the defaults
        will be used for the other steps.

        Example
        -------
        In this example, we instantiate a Launcher that uses the default
        class for each of the launching steps.

        >>> import fromconfig
        >>> config = {
        ...     "run": "local",
        ...     "log": "logging",
        ...     "parse": "parser",
        ...     "sweep": "hparams"
        ... }
        >>> launcher = fromconfig.launcher.DefaultLauncher.fromconfig(config)

        By specifying twice "logging" for the "log" step the resulting
        launcher will wrap the LoggingLauncher twice (resulting in a
        double logging).

        >>> import fromconfig
        >>> config = {
        ...     "log": ["logging", "logging"]
        ... }
        >>> launcher = fromconfig.launcher.DefaultLauncher.fromconfig(config)
        """
        if is_mapping(config) and any(key in config for key in _STEPS):
            if not all(key in _STEPS for key in config):
                raise ValueError(f"Either all keys or none should be in {_STEPS} but got {config}")
            config = [config.get(key, default) for key, default in _STEPS.items()]

        return super().fromconfig(config)
