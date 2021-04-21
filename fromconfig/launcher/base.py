"""Base class for launchers."""

from abc import ABC
from typing import Any, Mapping, Dict, Type
import inspect
import logging
import pkg_resources

from fromconfig.core.base import fromconfig, FromConfig, Keys
from fromconfig.utils.types import is_pure_iterable, is_mapping
from fromconfig.version import MAJOR


LOGGER = logging.getLogger(__name__)


class Launcher(FromConfig, ABC):
    """Base class for launchers."""

    def __init__(self, launcher: "Launcher"):
        self.launcher = launcher

    def __call__(self, config: Any, command: str = ""):
        """Launch implementation.

        Parameters
        ----------
        config : Any
            The config
        command : str, optional
            The fire command
        """
        raise NotImplementedError()

    @classmethod
    def fromconfig(cls, config: Mapping) -> "Launcher":
        """Custom fromconfig implementation.

        The config parameter can either be a plain config dictionary
        with special keys (like _attr_, etc.). In that case, it simply
        uses fromconfig to instantiate the corresponding class.

        It can also list launchers by name (set internally or plugin
        names for external launchers). In that case, it will compose
        the launchers (first item will be higher in the instance
        hierarchy).

        It can also be a dictionary with special keys run, log, parse
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
        >>> launcher = fromconfig.launcher.Launcher.fromconfig(config)

        By specifying twice "logging" for the "log" step the resulting
        launcher will wrap the LoggingLauncher twice (resulting in a
        double logging).

        >>> import fromconfig
        >>> config = {
        ...     "log": ["logging", "logging"]
        ... }
        >>> launcher = fromconfig.launcher.Launcher.fromconfig(config)

        Parameters
        ----------
        config : Mapping
            Typically a dictionary with keys run, log, parse and sweep.

        Returns
        -------
        Launcher
        """

        def _fromconfig(cfg, launcher: Launcher = None):
            # None case
            if cfg is None:
                return launcher

            # Launcher class name
            if isinstance(cfg, str):
                launcher_cls = _get_cls(cfg)
                return launcher_cls(launcher=launcher) if launcher else launcher_cls()  # type: ignore

            # List of launchers to compose (first item is highest)
            if is_pure_iterable(cfg):
                for item in cfg[::-1]:
                    launcher = _fromconfig(item, launcher)
                return launcher

            if is_mapping(cfg):
                # Special syntax by section
                keys = [("sweep", ["hparams"]), ("parse", ["parser"]), ("log", ["logging"]), ("run", ["local"])]
                if any(key in cfg for key, _ in keys):
                    for key, defaults in keys[::-1]:
                        launcher = _fromconfig(cfg.get(key, defaults), launcher=launcher)
                    return launcher

                # Special treatment for "launcher" key
                if "launcher" in cfg:
                    if launcher is not None:
                        raise ValueError(f"Launcher conflict, launcher is not None ({launcher}) but cfg={cfg}")
                    launcher = _fromconfig(cfg["launcher"])
                cfg = cfg if not launcher else {**cfg, "launcher": launcher}

                # Regular config
                if any(key in cfg for key in Keys):
                    return fromconfig(cfg)

                # Typical implementation
                return cls(**{key: fromconfig(value) for key, value in cfg.items()})

            if isinstance(cfg, Launcher):
                if launcher is not None:
                    raise ValueError(f"Launcher conflict, launcher is not None ({launcher}) but cfg={cfg}")
                return cfg

            raise TypeError(f"Unable to instantiate launcher from {cfg} (unsupported type {type(cfg)})")

        return _fromconfig(config)


# First call to _get_cls adds internal and external classes
_CLASSES: Dict[str, Type] = {}


def _get_cls(name: str) -> Type:
    """Load and return internal and external launcher classes."""
    if not _CLASSES:
        # pylint: disable=import-outside-toplevel,cyclic-import
        # Import internal classes
        from fromconfig.launcher.hparams import HParamsLauncher
        from fromconfig.launcher.parser import ParserLauncher
        from fromconfig.launcher.logger import LoggingLauncher
        from fromconfig.launcher.local import LocalLauncher
        from fromconfig.launcher.dry import DryLauncher

        # Create references with default names
        _CLASSES["local"] = LocalLauncher
        _CLASSES["logging"] = LoggingLauncher
        _CLASSES["hparams"] = HParamsLauncher
        _CLASSES["parser"] = ParserLauncher
        _CLASSES["dry"] = DryLauncher

        # Load external classes, use entry point's name for reference
        for entry_point in pkg_resources.iter_entry_points(f"fromconfig{MAJOR}"):
            module = entry_point.load()
            for _, cls in inspect.getmembers(module, lambda m: inspect.isclass(m) and issubclass(m, Launcher)):
                if entry_point.name in _CLASSES:
                    raise ValueError(f"Duplicate launcher name found {entry_point.name} ({_CLASSES})")
                _CLASSES[entry_point.name] = cls

        # Log loaded classes
        LOGGER.info(f"Loaded Launcher classes {_CLASSES}")

    if name not in _CLASSES:
        raise KeyError(f"Launcher class {name} not found in {_CLASSES}")
    return _CLASSES[name]
