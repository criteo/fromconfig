"""Tests for parser.reference."""

import pytest

import fromconfig


@pytest.mark.parametrize(
    "config, expected",
    [
        pytest.param({"x": 1, "y": 2}, {"x": 1, "y": 2}, id="none"),
        pytest.param({"x": 1, "y": "@x"}, {"x": 1, "y": 1}, id="simple"),
        pytest.param({"x": 1, "y": "@x", "z": "@y"}, {"x": 1, "y": 1, "z": 1}, id="dependency"),
        pytest.param({"x": 1, "y": {"z": "@x"}}, {"x": 1, "y": {"z": 1}}, id="nested-resolve"),
        pytest.param({"x": {"y": 1}, "z": "@x.y"}, {"x": {"y": 1}, "z": 1}, id="nested-reference"),
        pytest.param(
            {"x": {"_attr_": "Config", "y": 1}, "z": "@x"},
            {"x": {"_attr_": "Config", "y": 1}, "z": {"_attr_": "Config", "y": 1}},
            id="attr",
        ),
    ],
)
def test_parser_reference(config, expected):
    """Test parser.ReferenceParser."""
    parser = fromconfig.parser.ReferenceParser()
    assert parser(config) == expected
