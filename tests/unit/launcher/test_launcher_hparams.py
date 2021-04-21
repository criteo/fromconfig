"""Test for launcher.hparams."""

import fromconfig


def test_launcher_hparams():
    """Test HParamsLauncher."""
    got = []
    expected = [({"hparams": {"dim": 10}}, "command"), ({"hparams": {"dim": 100}}, "command")]

    def got_launcher(config, command):
        got.append((config, command))

    launcher = fromconfig.launcher.HParamsLauncher(got_launcher)
    config = {"hparams": {"dim": [10, 100]}}
    launcher(config, "command")
    assert got == expected
