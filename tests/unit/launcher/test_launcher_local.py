"""Test launcher.local."""

import pytest

import fromconfig


def test_launcher_local_init():
    """Test LocalLauncher initialization."""
    fromconfig.launcher.LocalLauncher()

    # Cannot nest two local launchers
    with pytest.raises(ValueError):
        fromconfig.launcher.LocalLauncher(fromconfig.launcher.LocalLauncher())


def test_launcher_local_basics():
    """Test basic functionality of the local launcher."""
    got = {}

    def run():
        got.update({"run": True})

    config = {"run": run}
    launcher = fromconfig.launcher.LocalLauncher()
    launcher(config, "run")
    assert got["run"]


@pytest.mark.parametrize(
    "config, command",
    [pytest.param(None, "", id="none"), pytest.param([], "", id="list"), pytest.param({"run": None}, "run", id="dict")],
)
def test_launcher_local_types(config, command):
    """Test that LocalLauncher accepts different types."""
    launcher = fromconfig.launcher.LocalLauncher()
    launcher(config, command)
