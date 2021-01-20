"""Tests for parser.__init__."""

import pytest

import fromconfig


@pytest.mark.parametrize(
    "config, expected", [pytest.param({"_attr_": "list", "_eval_": "partial", "_args_": [[1]]}, lambda: [1])]
)
def test_parser_parse(config, expected):
    """Test default parse."""
    parsed = fromconfig.parser.parse(config)
    if callable(expected):
        assert fromconfig.fromconfig(parsed)() == expected()
    else:
        assert fromconfig.fromconfig(parsed) == expected
