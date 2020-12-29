"""Test for parser.singleton."""

import fromconfig


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
