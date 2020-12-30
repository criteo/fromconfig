"""Tests for parser.__init__."""

import pytest

import fromconfig


@pytest.mark.parametrize(
    "config, expected",
    [
        pytest.param(
            {"_macro_": {"x": 1}, "_config_": {"_attr_": "list", "_eval_": "partial", "_args_": [["@x"]]}}, lambda: [1]
        )
    ],
)
def test_parser_parse(config, expected):
    """Test default parse."""
    parsed = fromconfig.parser.parse(config)
    if callable(expected):
        assert fromconfig.fromconfig(parsed)() == expected()
    else:
        assert fromconfig.fromconfig(parsed) == expected
