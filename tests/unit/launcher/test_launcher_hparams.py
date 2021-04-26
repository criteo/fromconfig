"""Test for launcher.hparams."""

import pytest

import fromconfig


@pytest.mark.parametrize(
    "config, command, expected",
    [
        pytest.param(
            {"hparams": {"dim": [10, 100]}},
            "command",
            [({"hparams": {"dim": 10}}, "command"), ({"hparams": {"dim": 100}}, "command")],
            id="dict",
        ),
        pytest.param([], "command", [([], "command")], id="list"),
        pytest.param(None, "command", [(None, "command")], id="none"),
    ],
)
def test_launcher_hparams(config, command, expected):
    """Test HParamsLauncher."""
    got = []

    def got_launcher(config, command):
        got.append((config, command))

    launcher = fromconfig.launcher.HParamsLauncher(got_launcher)
    launcher(config, command)
    assert got == expected
