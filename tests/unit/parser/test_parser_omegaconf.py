"""Test for parser.omega"""

import pytest

import fromconfig


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
def test_parser_omega(resolvers, error):
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
