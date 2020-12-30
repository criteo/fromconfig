"""Tests for parser.macro."""

import pytest

import fromconfig


@pytest.mark.parametrize(
    "config, expected",
    [
        pytest.param({"x": 1}, {"x": 1}, id="none"),
        pytest.param({"_config_": {"x": 1}}, {"x": 1}, id="config"),
        pytest.param({"_macro_": {"x": 1}}, {}, id="macro"),
        pytest.param({"_macro_": {"x": 2}, "_config_": {"x": 1, "y": "@x"}}, {"x": 1, "y": 2}, id="macro+config"),
    ],
)
def test_parser_macro(config, expected):
    """Test parser.MacroParser."""
    parser = fromconfig.parser.MacroParser()
    assert parser(config) == expected


@pytest.mark.parametrize(
    "config, error",
    [
        pytest.param({"_macro_": [1], "_config_": {}}, TypeError, id="macro+list"),
        pytest.param({"_macro_": 1, "_config_": {}}, TypeError, id="macro+int"),
        pytest.param({"_macro_": "hello", "_config_": {}}, TypeError, id="macro+string"),
        pytest.param({"_macro_": None, "_config_": {}}, TypeError, id="macro+none"),
        pytest.param(
            {"_macro_": {"x": 1}, "_config_": {"y": "@x"}, "other": "forbidden"}, ValueError, id="config+macro+other"
        ),
    ],
)
def test_parser_macro_type_error(config, error):
    """Test parser.MacroParser type errors."""
    parser = fromconfig.parser.MacroParser()
    with pytest.raises(error):
        parser(config)
