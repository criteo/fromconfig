"""Test for parser.omega"""

import fromconfig


def hello(s):
    return f"hello {s}"


def test_parser_omega():
    """Test OmegaConfParser."""
    config = {"hello_world": "${hello:world}", "date": "${now:}", "resolvers": {"hello": "hello"}}
    parser = fromconfig.parser.OmegaConfParser()
    parsed = parser(config)
    assert parsed["hello_world"] == "hello world"  # Custom resolver
    assert "$" not in parsed["date"]  # Make sure now was resolved
