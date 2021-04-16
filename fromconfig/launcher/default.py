"""Default Launcher."""

from typing import Any, Mapping, List, Tuple, Type
import pkg_resources
import inspect

from fromconfig.version import MAJOR
from fromconfig.core.base import Keys, fromconfig, FromConfig
from fromconfig.launcher.hparams import HParamsLauncher
from fromconfig.launcher.parser import ParserLauncher
from fromconfig.launcher.logger import LoggingLauncher
from fromconfig.launcher.local import LocalLauncher
from fromconfig.utils.nest import merge_dict
from fromconfig.launcher import base


class DefaultLauncher(base.Launcher, FromConfig):
    """Default Launcher."""

    def __init__(self, launcher: base.Launcher = None):
        self.launcher = launcher or HParamsLauncher(ParserLauncher(LoggingLauncher(LocalLauncher())))

    def setup(self):
        self.launcher.setup()

    def launch(self, config: Any, command: str = "", parsed: Any = None):
        self.launcher.launch(config=config, command=command, parsed=parsed)

    def teardown(self):
        self.launcher.teardown()

    @classmethod
    def fromconfig(cls, config: Mapping):
        # Nothing specified, use default
        if not config:
            return cls()

        # The launcher is a regular config, in that case instantiate
        if any(key in config for key in Keys):
            return fromconfig(config)
        if "launcher" in config:
            return cls(fromconfig(config["launcher"]))

        # Instantiate launcher from config
        launcher = _instantiate_class(config.get("runner", "default"), base.RunLauncher)
        launcher = _instantiate_class(config.get("logger", "default"), base.LogLauncher, launcher=launcher)
        launcher = _instantiate_class(config.get("parser", "default"), base.ParseLauncher, launcher=launcher)
        launcher = _instantiate_class(config.get("sweeper", "default"), base.SweepLauncher, launcher=launcher)
        return cls(launcher)


_CLASSES: List[Tuple[str, Type]] = []


def _classes() -> List[Tuple[str, Type]]:
    """Load and return internal and external launcher classes."""
    if not _CLASSES:
        # Load internal classes
        for cls in [LocalLauncher, LoggingLauncher, HParamsLauncher, ParserLauncher]:
            _CLASSES.append(("default", cls))

        # Load external classes
        for entry_point in pkg_resources.iter_entry_points(f"fromconfig{MAJOR}"):
            module = entry_point.load()
            for _, cls in inspect.getmembers(module, lambda m: inspect.isclass(m) and issubclass(m, base.Launcher)):
                _CLASSES.append((entry_point.name, cls))

    return _CLASSES


def _instantiate_class(config, classinfo: Type, launcher: base.Launcher = None) -> base.Launcher:
    if isinstance(config, (str, list)):
        names = [config] if isinstance(config, str) else config
        for name in names[::-1]:
            launcher_cls = _get_class(name, classinfo)
            launcher = launcher_cls(launcher=launcher) if launcher else launcher_cls()
    else:
        config = merge_dict({"launcher": launcher}, config) if launcher else config
        launcher = fromconfig(config)
    return launcher


def _get_class(name: str, classinfo: Type) -> base.Launcher:
    """Get launcher of type base with name in launchers."""
    for cls_name, cls in _classes():
        if cls_name == name and issubclass(cls, classinfo):
            return cls
    raise ValueError(f"Unable to find class of name {name} and type {classinfo} in {_classes()}")
