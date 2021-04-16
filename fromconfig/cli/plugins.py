"""Load plugins."""

from typing import Mapping
import pkg_resources
import inspect
import collections

from fromconfig.core.base import fromconfig, FromConfig
from fromconfig.launcher.base import Launcher, RunLauncher, LogLauncher, ParseLauncher, SweepLauncher
from fromconfig.launcher.local import LocalLauncher
from fromconfig.launcher.logger import LoggingLauncher
from fromconfig.launcher.hparams import HParamsLauncher
from fromconfig.launcher.parser import ParserLauncher
from fromconfig.utils.nest import merge_dict
from fromconfig.version import MAJOR


class Plugins(FromConfig):
    """Plugins."""

    def __init__(self, launcher: Launcher):
        self.launcher = launcher

    @classmethod
    def fromconfig(cls, config: Mapping):
        # FromConfig definition of the launcher
        if "launcher" in config:
            return cls(fromconfig(config["launcher"]))

        # Look for Launcher classes defined in plugins
        defaults = [LocalLauncher, LoggingLauncher, HParamsLauncher, ParserLauncher]
        classes = [("default", default_cls) for default_cls in defaults]
        for entry_point in pkg_resources.iter_entry_points(f"fromconfig{MAJOR}"):
            module = entry_point.load()
            for _, member in inspect.getmembers(module, lambda c: inspect.isclass(c) and issubclass(c, Launcher)):
                classes.append((entry_point.name, member))

        # Distribute classes by base
        bases = [
            ("runner", RunLauncher),
            ("logger", LogLauncher),
            ("parser", ParseLauncher),
            ("sweeper", SweepLauncher),
        ]
        classes_by_base = collections.defaultdict(dict)
        for name, launcher_cls in classes:
            for _, base_cls in bases:
                if issubclass(launcher_cls, base_cls):
                    classes_by_base[base_cls][name] = launcher_cls

        # Instantiate launcher from config
        launcher = None
        for base_key, base_cls in bases:
            cfg = config.get(base_key, "default")
            if isinstance(cfg, (str, list)):
                names = [cfg] if isinstance(cfg, str) else cfg
                for name in names[::-1]:
                    launcher_cls = classes_by_base[base_cls][name]
                    launcher = launcher_cls(launcher=launcher) if launcher else launcher_cls()
            else:
                cfg = merge_dict({"launcher": launcher}, cfg) if launcher else cfg
                launcher = fromconfig(cfg)

        return cls(launcher)
