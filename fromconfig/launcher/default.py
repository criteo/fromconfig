"""Default Launcher."""

from typing import Any
import pkg_resources
import inspect
import collections

from fromconfig.core.base import fromconfig
from fromconfig.launcher import base
from fromconfig.launcher.local import LocalLauncher
from fromconfig.launcher.logger import LoggingLauncher
from fromconfig.launcher.params import ParamsLauncher
from fromconfig.launcher.parser import ParserLauncher
from fromconfig.utils.nest import merge_dict


class DefaultLauncher(base.Launcher):
    """Default Launcher."""

    def __init__(self):
        self.launcher = ParamsLauncher(launcher=ParserLauncher(launcher=LoggingLauncher(launcher=LocalLauncher())))

    def __call__(self, config: Any, parsed: Any = None, command: str = ""):
        self.launcher(config=config, parsed=parsed, command=command)


def init(config):
    # Look for Launcher classes defined in plugins
    classes = [("default", cls) for cls in [LocalLauncher, LoggingLauncher, ParamsLauncher, ParserLauncher]]
    for entry_point in pkg_resources.iter_entry_points("fromconfig0"):
        module = entry_point.load()
        for _, cls in inspect.getmembers(module, lambda c: inspect.isclass(c) and issubclass(c, base.Launcher)):
            classes.append((entry_point.name, cls))

    # Distribute classes by base
    bases = [
        ("runner", base.RunLauncher),
        ("logger", base.LogLauncher),
        ("parser", base.ParseLauncher),
        ("sweeper", base.SweepLauncher)
    ]
    classes_by_base = collections.defaultdict(dict)
    for name, cls in classes:
        for _, base_cls in bases:
            if issubclass(cls, base_cls):
                classes_by_base[base_cls][name] = cls

    # Instantiate launcher from config
    launcher = None
    for base_key, base_cls in bases:
        cfg = config.get(base_key, "default")
        if isinstance(cfg, (str, list)):
            names = [cfg] if isinstance(cfg, str) else cfg
            for name in names[::-1]:
                cls = classes_by_base[base_cls][name]
                launcher = cls(launcher=launcher) if launcher else cls()
        else:
            cfg = merge_dict({"launcher": launcher}, cfg) if launcher else cfg
            launcher = fromconfig(cfg)
    return launcher
