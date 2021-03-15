"""Tests for parser.reference."""

import pytest

import fromconfig


@pytest.mark.parametrize(
    "config, expected",
    [
        pytest.param({"x": 1, "y": 2}, {"x": 1, "y": 2}, id="none"),
        pytest.param({"x": 1, "y": "@x"}, {"x": 1, "y": 1}, id="simple"),
        pytest.param({"x": 1, "y": "@x", "z": "@x"}, {"x": 1, "y": 1, "z": 1}, id="double"),
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


@pytest.mark.parametrize(
    "config,exception",
    [
        pytest.param({"x": "@y"}, KeyError, id="key-simple"),
        pytest.param({"x": {"y": "@z"}}, KeyError, id="key-nested"),
        pytest.param({"x": [0], "y": "@x[1]"}, IndexError, id="list-simple"),
        pytest.param({"x": {"y": [0]}, "y": "@x.y[1]"}, IndexError, id="list-nested"),
        pytest.param({"x": "@y", "y": "@x"}, ValueError, id="cycle-simple"),
        pytest.param({"x": {"y": "@z"}, "z": "@x"}, ValueError, id="cycle-nested"),
        pytest.param({"x": {"y": "@z"}, "z": "@x.y"}, ValueError, id="cycle-nested-2"),
    ],
)
def test_parser_reference_exceptions(config, exception):
    """Test parser.ReferenceParser exceptions."""
    parser = fromconfig.parser.ReferenceParser()
    with pytest.raises(exception):
        parser(config)


@pytest.mark.parametrize(
    "item,expected",
    [
        pytest.param("@x", True, id="reference"),
        pytest.param("x", False, id="string"),
        pytest.param("x@", False, id="string+@"),
        pytest.param(1, False, id="int"),
        pytest.param({"@x": 1}, False, id="dict"),
    ],
)
def test_parser_reference_is_reference(item, expected):
    """Test parser.reference.is_reference."""
    assert fromconfig.parser.reference.is_reference(item) == expected


@pytest.mark.parametrize(
    "item,expected",
    [
        pytest.param("@x", ["x"], id="simple"),
        pytest.param("@x.y", ["x", "y"], id="double"),
        pytest.param("@x[0]", ["x", 0], id="simple+list"),
        pytest.param("@x.y[0]", ["x", "y", 0], id="double+list"),
        pytest.param("@x[0].y", ["x", 0, "y"], id="simple+list+simple"),
    ],
)
def test_parser_reference_to_keys(item, expected):
    """Test parser.reference.reference_to_keys."""
    assert fromconfig.parser.reference.reference_to_keys(item) == expected
