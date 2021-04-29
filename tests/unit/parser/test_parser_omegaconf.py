"""Test for parser.omega"""

import pytest

import fromconfig


@pytest.mark.parametrize(
    "config, expected",
    [
        pytest.param(None, None, id="none"),
        pytest.param({"foo": "bar"}, {"foo": "bar"}, id="none"),
        pytest.param({"foo": "bar", "baz": "${foo}"}, {"foo": "bar", "baz": "bar"}, id="vanilla"),
    ],
)
def test_parser_omega(config, expected):
    """Test that OmegaConfParser accepts different types."""
    parser = fromconfig.parser.OmegaConfParser()
    assert parser(config) == expected


def hello(s):
    return f"hello {s}"


@pytest.mark.parametrize(
    "resolvers, error",
    [
        pytest.param({"hello": "hello"}, False),
        pytest.param({"hello": {"_attr_": "fromconfig.utils.from_import_string", "_args_": ["hello"]}}, False),
        pytest.param({"hello": ["hello"]}, True),
    ],
)
def test_parser_omega_resolvers(resolvers, error):
    """Test OmegaConfParser."""
    config = {"hello_world": "${hello:world}", "date": "${now:}", "resolvers": resolvers}
    parser = fromconfig.parser.OmegaConfParser()
    if error:
        with pytest.raises(Exception):
            parsed = parser(config)
    else:
        parsed = parser(config)
        assert parsed["hello_world"] == "hello world"  # Custom resolver
        assert "$" not in parsed["date"]  # Make sure now was resolved
