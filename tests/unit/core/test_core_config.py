"""Tests for core.config."""

import pytest

import fromconfig


def test_config():
    """Test Config."""
    config = fromconfig.Config(x=1)
    assert config["x"] == 1
    assert list(config) == ["x"]
    config["x"] = 2
    assert config["x"] == 2


@pytest.mark.parametrize(
    "config, expected",
    [
        pytest.param(
            {"_attr_": "str", "_args_": "hello"}, fromconfig.Config(_attr_="str", _args_="hello"), id="simple"
        ),
        pytest.param(
            {"config": {"_attr_": "str", "_args_": "hello"}},
            fromconfig.Config(_attr_="str", _args_="hello"),
            id="config",
        ),
    ],
)
def test_config_fromconfig_method(config, expected):
    """Test Config.fromconfig."""
    assert fromconfig.Config.fromconfig(config) == expected


@pytest.mark.parametrize(
    "config, expected",
    [
        pytest.param(
            {"_attr_": "Config", "config": {"_attr_": "str", "_args_": "hello"}},
            fromconfig.Config(_attr_="str", _args_="hello"),
            id="config-with-attr",
        )
    ],
)
def test_config_fromconfig(config, expected):
    """Test fromconfig on Config config."""
    assert fromconfig.fromconfig(config) == expected
