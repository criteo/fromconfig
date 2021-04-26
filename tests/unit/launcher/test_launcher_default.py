"""Test for launcher.default."""

import pytest

import fromconfig


def assert_equal_launcher(a, b):
    assert type(a) is type(b)
    if a.launcher is not None or b.launcher is not None:
        assert_equal_launcher(a.launcher, b.launcher)


@pytest.mark.parametrize(
    "config, expected",
    [
        pytest.param({"sweep": [], "log": [], "parse": []}, fromconfig.launcher.LocalLauncher(), id="only-run-list"),
        pytest.param(
            {"sweep": None, "log": None, "parse": None}, fromconfig.launcher.LocalLauncher(), id="only-run-none"
        ),
        pytest.param({"sweep": "hparams", "unknown-step": "local"}, ValueError, id="unknown-step"),
    ],
)
def test_launcher_default_fromconfig(config, expected):
    """Test custom fromconfig support."""
    if isinstance(expected, fromconfig.launcher.Launcher):
        assert_equal_launcher(fromconfig.launcher.DefaultLauncher.fromconfig(config), expected)
    else:
        with pytest.raises(expected):
            fromconfig.launcher.DefaultLauncher.fromconfig(config)
