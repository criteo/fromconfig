"""Test launcher.dry."""

import pytest

import fromconfig


@pytest.mark.parametrize(
    "config, command",
    [
        pytest.param({"foo": "bar"}, "foo", id="dict"),
        pytest.param(None, "", id="none"),
        pytest.param(["foo"], "", id="list"),
    ],
)
def test_launcher_dry(config, command):
    """Test dry launcher."""
    launcher = fromconfig.launcher.DryLauncher()
    launcher(config, command)
