"""Tests for parser.__init__."""

import pytest

import fromconfig


@pytest.mark.parametrize(
    "config, expected", [pytest.param({"_attr_": "list", "_eval_": "partial", "_args_": [[1]]}, lambda: [1])]
)
def test_parser_default_parser(config, expected):
    """Test default parse."""
    parser = fromconfig.parser.DefaultParser()
    parsed = parser(config)
    if callable(expected):
        assert fromconfig.fromconfig(parsed)() == expected()
    else:
        assert fromconfig.fromconfig(parsed) == expected
