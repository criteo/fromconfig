"""Base class for launchers."""

from abc import ABC
from typing import Any, Dict, Type
import inspect
import logging
import pkg_resources

from fromconfig.core.base import fromconfig, FromConfig, Keys
from fromconfig.utils.libimport import from_import_string
from fromconfig.utils.nest import merge_dict
from fromconfig.utils.types import is_pure_iterable, is_mapping
from fromconfig.version import __major__


LOGGER = logging.getLogger(__name__)

# Internal and external Launcher classes referenced by name
_CLASSES: Dict[str, Type] = {}  # Loaded during first _classes() call


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

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.launcher})"

    @classmethod
    def fromconfig(cls, config: Any) -> "Launcher":
        """Custom fromconfig implementation.

        The config parameter can either be a plain config dictionary
        with special keys (like _attr_, etc.). In that case, it simply
        uses fromconfig to instantiate the corresponding class.

        It can also list launchers by name (set internally or plugin
        names for external launchers). In that case, it will compose
        the launchers (first item will be higher in the instance
        hierarchy).

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

            # Already a Launcher
            if isinstance(cfg, Launcher):
                if launcher is not None:
                    raise ValueError(f"Cannot wrap launchers, launcher is not None ({launcher}) but cfg={cfg}")
                return cfg

            # Launcher class name with no other parameters
            if isinstance(cfg, str):
                launcher_cls = _classes()[cfg]
                return launcher_cls(launcher=launcher) if launcher else launcher_cls()  # type: ignore

            # List of launchers to compose (first item is highest)
            if is_pure_iterable(cfg):
                for item in reversed(cfg):
                    launcher = _fromconfig(item, launcher)
                return launcher

            if is_mapping(cfg):
                # Resolve the class from ATTR key, default to parent
                if Keys.ATTR in cfg:
                    if cfg[Keys.ATTR] in _classes():
                        launcher_cls = _classes()[cfg[Keys.ATTR]]
                    else:
                        launcher_cls = from_import_string(cfg[Keys.ATTR])
                else:
                    launcher_cls = cls

                # Special treatment for "launcher" key if present
                if "launcher" in cfg:
                    if launcher is not None:
                        raise ValueError(f"Cannot wrap launchers, launcher is not None ({launcher}) but cfg={cfg}")
                    launcher = _fromconfig(cfg["launcher"])
                cfg = cfg if not launcher else merge_dict(cfg, {"launcher": launcher})

                # Instantiate positional and keyword arguments
                args = fromconfig(cfg.get(Keys.ARGS, []))
                kwargs = {key: fromconfig(value) for key, value in cfg.items() if key not in Keys}
                return launcher_cls(*args, **kwargs)  # type: ignore

            raise TypeError(f"Unable to instantiate launcher from {cfg} (unsupported type {type(cfg)})")

        return _fromconfig(config)


def _classes() -> Dict[str, Type]:
    """Load and return internal and external classes."""
    if not _CLASSES:
        _load()
    return _CLASSES


def _load():
    """Load internal and external classes into _CLASSES."""
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
    for entry_point in pkg_resources.iter_entry_points(f"fromconfig{__major__}"):
        module = entry_point.load()
        for _, cls in inspect.getmembers(module, lambda m: inspect.isclass(m) and issubclass(m, Launcher)):
            name = f"{entry_point.name}.{cls.NAME}" if hasattr(cls, "NAME") else entry_point.name
            if name in _CLASSES:
                raise ValueError(f"Duplicate launcher name found {name} ({_CLASSES})")
            _CLASSES[name] = cls

    # Log loaded classes
    LOGGER.info(f"Loaded Launcher classes {_CLASSES}")
