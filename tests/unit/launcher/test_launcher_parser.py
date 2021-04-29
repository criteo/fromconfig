"""Test launcher.parser."""

import pytest

import fromconfig


@pytest.mark.parametrize(
    "config, expected",
    [
        pytest.param(None, None, id="none"),
        pytest.param({"foo": "bar"}, {"foo": "bar"}, id="dict"),
        pytest.param(["foo"], ["foo"], id="list"),
        pytest.param({"foo": "bar", "baz": "${foo}"}, {"foo": "bar", "baz": "bar"}, id="parsed"),
        pytest.param({"foo": "bar", "baz": "${foo}", "parser": None}, {"foo": "bar", "baz": "${foo}"}, id="no-parser"),
    ],
)
def test_launcher_parser(config, expected):
    """Test ParserLauncher."""
    got = {}

    def capture(config, command=""):
        # pylint: disable=unused-argument
        got.update({"result": config})

    launcher = fromconfig.launcher.ParserLauncher(capture)
    launcher(config)
    assert got["result"] == expected
