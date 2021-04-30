"""Test launcher.logger."""

import logging

import pytest

import fromconfig


@pytest.mark.parametrize(
    "config, expected",
    [
        pytest.param({"foo": "bar"}, ({}, []), id="default"),
        pytest.param(None, ({}, []), id="none"),
        pytest.param({"foo": "bar", "logging": {"level": 20}}, ({"level": 20}, []), id="set-level"),
    ],
)
def test_launcher_logger(config, expected, monkeypatch):
    """Basic Test for LoggingLauncher."""
    basic_config = {}
    logs = []

    class MonkeyLogger:
        def info(self, msg):
            logs.append(msg)

    def MonkeyBasicConfig(**kwargs):  # pylint: disable=invalid-name
        basic_config.update(kwargs)

    monkeypatch.setattr(logging, "basicConfig", MonkeyBasicConfig)
    monkeypatch.setattr(fromconfig.launcher.logger, "LOGGER", MonkeyLogger())

    launcher = fromconfig.launcher.LoggingLauncher(fromconfig.launcher.DryLauncher())
    launcher(config)
    assert (basic_config, logs) == expected
