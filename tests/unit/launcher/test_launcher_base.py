"""Test launcher.base."""

import pytest

from fromconfig.launcher.base import _get_cls
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
def test_get_cls(name, expected):
    """Test _get_cls."""
    if issubclass(expected, fromconfig.launcher.Launcher):
        assert _get_cls(name) is expected
    else:
        with pytest.raises(expected):
            _get_cls(name)


@pytest.mark.parametrize(
    "config, expected",
    [
        pytest.param("local", LocalLauncher(), id="local"),
        pytest.param("dry", DryLauncher(), id="dry"),
        pytest.param(
            ["hparams", "parser", "logging", "local"],
            HParamsLauncher(ParserLauncher(LoggingLauncher(LocalLauncher()))),
            id="hparams+parser",
        ),
        pytest.param({"sweep": [], "log": [], "parse": []}, LocalLauncher(), id="only-run"),
        pytest.param({"_attr_": "fromconfig.launcher.LocalLauncher"}, LocalLauncher(), id="fromconfig"),
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
