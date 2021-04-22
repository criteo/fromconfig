"""Test for parser.omega"""

import fromconfig


def hello(s):
    return f"hello {s}"


def test_parser_omega():
    """Test OmegaConfParser."""
    config = {"hello_world": "${hello:world}", "date": "${now:}"}
    parser = fromconfig.parser.OmegaConfParser({"hello": "hello"})
    parsed = parser(config)
    assert parsed["hello_world"] == "hello world"  # Custom resolver
    assert "$" not in parsed["date"]  # Make sure now was resolved
