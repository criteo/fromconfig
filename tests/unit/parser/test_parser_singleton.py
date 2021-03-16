"""Test for parser.singleton."""

import pytest

import fromconfig


class Class:
    """Class."""


def test_parser_singleton_constructor():
    """Test parser.singleton decorator."""
    x = fromconfig.parser.singleton("name", Class)
    y = fromconfig.parser.singleton("name", Class)
    z = fromconfig.parser.singleton("name")
    assert id(x) == id(y) == id(z)


def test_parser_singleton_constructor_missing():
    """Test parser.singleton decorator with missing constructor."""
    with pytest.raises(ValueError):
        fromconfig.parser.singleton("missing_constructor")


def test_parser_singleton_constructor_no_override():
    """Test parser.singleton decorator raises error with override."""
    fromconfig.parser.singleton("name", Class)
    with pytest.raises(KeyError):
        fromconfig.parser.singleton["name"] = Class


def test_parser_singleton():
    """Test parser.SingletonParser."""
    parser = fromconfig.parser.SingletonParser()
    config = {
        "x": {"_attr_": "dict", "_singleton_": "my_dict", "a": "a"},
        "y": {"_attr_": "dict", "_singleton_": "my_dict", "a": "a"},
    }
    parsed = parser(config)
    instance = fromconfig.fromconfig(parsed)
    x = instance["x"]
    y = instance["y"]
    expected = {"a": "a"}
    assert x == y == expected
    assert id(x) == id(y)
