"""Tests for core.config."""

import yaml
import json

import pytest

import fromconfig


def test_config():
    """Test Config."""
    config = fromconfig.Config(x=1)
    assert config["x"] == 1
    assert list(config) == ["x"]
    config["x"] = 2
    assert config["x"] == 2


@pytest.mark.parametrize("data, expected", [(yaml.dump({"x": 1}), {"x": 1}), (json.dumps({"x": 1}), {"x": 1})])
def test_config_loads(data, expected):
    """Test Config.loads."""
    assert fromconfig.Config.loads(data) == expected


@pytest.mark.parametrize(
    "config, expected",
    [
        ({"_attr_": "str", "_args_": "hello"}, fromconfig.Config(_attr_="str", _args_="hello")),
        ({"config": {"_attr_": "str", "_args_": "hello"}}, fromconfig.Config(_attr_="str", _args_="hello")),
    ],
)
def test_config_fromconfig_method(config, expected):
    """Test Config.fromconfig."""
    assert fromconfig.Config.fromconfig(config) == expected


@pytest.mark.parametrize(
    "config, expected",
    [
        (
            {"_attr_": "Config", "config": {"_attr_": "str", "_args_": "hello"}},
            fromconfig.Config(_attr_="str", _args_="hello"),
        )
    ],
)
def test_config_fromconfig(config, expected):
    """Test fromconfig on Config config."""
    assert fromconfig.fromconfig(config) == expected
