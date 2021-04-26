# pylint: disable=protected-access
"""Test launcher.base."""

import pytest
import pkg_resources
from typing import Any

import fromconfig

from fromconfig.launcher import HParamsLauncher
from fromconfig.launcher import ParserLauncher
from fromconfig.launcher import LoggingLauncher
from fromconfig.launcher import LocalLauncher
from fromconfig.launcher import DryLauncher


def assert_equal_launcher(a, b):
    assert type(a) is type(b)
    if a.launcher is not None or b.launcher is not None:
        assert_equal_launcher(a.launcher, b.launcher)


def test_launcher_is_abstract():
    with pytest.raises(NotImplementedError):
        fromconfig.launcher.Launcher(None)({})


@pytest.mark.parametrize(
    "name, expected",
    [
        pytest.param("hparams", HParamsLauncher, id="hparams"),
        pytest.param("parser", ParserLauncher, id="parser"),
        pytest.param("logging", LoggingLauncher, id="logging"),
        pytest.param("local", LocalLauncher, id="local"),
        pytest.param("does not exists", KeyError, id="missing-key"),
    ],
)
def test_launcher_classes(name, expected):
    """Test _get_cls."""
    if issubclass(expected, fromconfig.launcher.Launcher):
        assert fromconfig.launcher.base._classes()[name] is expected
    else:
        with pytest.raises(expected):
            fromconfig.launcher.base._classes()[name]  # pylint: disable=expression-not-assigned


def test_launcher_classes_extension(monkeypatch):
    """Test launcher classes extension."""

    fromconfig.launcher.base._CLASSES.clear()  # Clear internal and external launchers

    class DummyModule:
        class DummyLauncher(fromconfig.launcher.Launcher):
            def __call__(self, config: Any, command: str = ""):
                ...

    class EntryPoint:
        def __init__(self, name, module):
            self.name = name
            self.module = module

        def load(self):
            return self.module

    # Test discovery
    monkeypatch.setattr(pkg_resources, "iter_entry_points", lambda *_: [EntryPoint("dummy", DummyModule)])
    fromconfig.launcher.base._load()
    fromconfig.utils.testing.assert_launcher_is_discovered("dummy", DummyModule.DummyLauncher)
    assert fromconfig.launcher.base._classes()["dummy"] == DummyModule.DummyLauncher

    # Test that loading again causes errors because of duplicates
    with pytest.raises(ValueError):
        fromconfig.launcher.base._load()


@pytest.mark.parametrize(
    "config, expected",
    [
        pytest.param("local", LocalLauncher(), id="local"),
        pytest.param("dry", DryLauncher(), id="dry"),
        pytest.param(DryLauncher(), DryLauncher(), id="dry-instance"),
        pytest.param(
            ["hparams", "parser", "logging", "local"],
            HParamsLauncher(ParserLauncher(LoggingLauncher(LocalLauncher()))),
            id="hparams+parser+logging+local",
        ),
        pytest.param({"_attr_": "fromconfig.launcher.LocalLauncher"}, LocalLauncher(), id="fromconfig"),
        pytest.param({"_attr_": "local"}, LocalLauncher(), id="fromconfig-short"),
        pytest.param(
            {"_attr_": "fromconfig.launcher.HParamsLauncher", "launcher": "local"},
            HParamsLauncher(LocalLauncher()),
            id="fromconfig+nested",
        ),
        pytest.param(
            [{"_attr_": "fromconfig.launcher.HParamsLauncher", "launcher": "local"}, "local"],
            ValueError,
            id="fromconfig+nested-duplicate",
        ),
        pytest.param(
            [HParamsLauncher(None), "local"], ValueError, id="fromconfig+nested+already-instantiated-cannot-wrap",
        ),
        pytest.param(1, TypeError, id="incorrect-type"),
    ],
)
def test_launcher_fromconfig(config, expected):
    """Test custom fromconfig support."""
    if isinstance(expected, fromconfig.launcher.Launcher):
        assert_equal_launcher(fromconfig.launcher.Launcher.fromconfig(config), expected)
    else:
        with pytest.raises(expected):
            fromconfig.launcher.Launcher.fromconfig(config)
