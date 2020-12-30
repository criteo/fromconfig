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


@pytest.mark.parametrize(
    "config, allow_missing, expected",
    [
        pytest.param({"x": 1, "y": "@x"}, False, {"x": 1, "y": 1}, id="ok+false"),
        pytest.param({"x": 1, "y": "@x"}, True, {"x": 1, "y": 1}, id="ok+true"),
        pytest.param({"y": "@x"}, True, {"y": "@x"}, id="missing+true"),
        pytest.param({"y": "@x"}, False, KeyError, id="missing+true"),
    ],
)
def test_parser_reference_allow_missing(config, allow_missing, expected):
    """Test parser.ReferenceParser with allow_missing."""
    parser = fromconfig.parser.ReferenceParser(allow_missing=allow_missing)
    if expected is KeyError:
        with pytest.raises(KeyError):
            parser(config)
    else:
        assert parser(config) == expected


@pytest.mark.parametrize(
    "config, keys, expected",
    [
        pytest.param({"x": 1, "y": "@x"}, None, {"x": 1, "y": 1}, id="default"),
        pytest.param({"x": 1, "y": "@x"}, ["x"], {"x": 1, "y": 1}, id="x"),
        pytest.param(
            {"x": 1, "y": 2, "xx": "@x", "yy": "@y"}, ["x"], {"x": 1, "y": 2, "xx": 1, "yy": "@y"}, id="x+(not)y"
        ),
        pytest.param(
            {"x": 1, "y": 2, "xx": "@x", "yy": "@y"}, ["y"], {"x": 1, "y": 2, "xx": "@x", "yy": 2}, id="(not)x+y"
        ),
        pytest.param(
            {"x": 1, "y": 2, "xx": "@x", "yy": "@y"}, ["x", "y"], {"x": 1, "y": 2, "xx": 1, "yy": 2}, id="x+y"
        ),
    ],
)
def test_parser_reference_keys(config, keys, expected):
    """Test parser.ReferenceParser with select keys."""
    parser = fromconfig.parser.ReferenceParser(keys=keys, allow_missing=True)
    if expected is KeyError:
        with pytest.raises(KeyError):
            parser(config)
    else:
        assert parser(config) == expected


@pytest.mark.parametrize(
    "item, expected",
    [
        pytest.param("@x", True, id="reference"),
        pytest.param("x", False, id="string"),
        pytest.param("x@", False, id="string+@"),
        pytest.param(1, False, id="int"),
        pytest.param({"@x": 1}, False, id="dict"),
    ],
)
def test_parser_reference_is_reference(item, expected):
    """Test parser.ReferenceParser.is_reference."""
    parser = fromconfig.parser.ReferenceParser()
    assert parser.is_reference(item) == expected


@pytest.mark.parametrize(
    "item, expected", [pytest.param("@x", "x", id="reference"), pytest.param("x", ValueError, id="reference")]
)
def test_parser_reference_get_reference(item, expected):
    """Test parser.ReferenceParser.get_reference."""
    parser = fromconfig.parser.ReferenceParser()
    if expected is ValueError:
        with pytest.raises(ValueError):
            parser.get_reference(item)
    else:
        assert parser.get_reference(item) == expected
