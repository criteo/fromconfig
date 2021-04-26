"""Test for parser.base."""

import pytest

import fromconfig


def test_parser_parser_class_is_abstract():
    """Test that from config is abstract."""
    with pytest.raises(Exception):
        fromconfig.parser.Parser()  # pylint: disable=abstract-class-instantiated

    with pytest.raises(NotImplementedError):
        fromconfig.parser.Parser.__call__(None, {"x": 1})


def test_parser_chain():
    """Test Chain Parser."""

    class MockParser(fromconfig.parser.Parser):
        def __init__(self, value):
            self.value = value

        def __repr__(self):
            return str(self.value)

        def __call__(self, config):
            config["value"] = self.value
            config["sum"] += self.value
            return config

    parser = fromconfig.parser.ChainParser(MockParser(1), MockParser(2))
    got = parser({"value": None, "sum": 0})
    assert got == {"value": 2, "sum": 3}
    assert repr(parser) == "ChainParser(1, 2)"
