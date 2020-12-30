"""Tests for core.base."""

import pytest

import fromconfig


def test_core_fromconfig_abstract():
    """Test that from config is abstract."""
    with pytest.raises(Exception):
        fromconfig.FromConfig()  # pylint: disable=abstract-class-instantiated

    with pytest.raises(NotImplementedError):
        fromconfig.FromConfig.fromconfig({"x": 1})


@fromconfig.register("Custom")
class Custom(fromconfig.FromConfig):
    """Custom FromConfig class."""

    def __init__(self, x):
        self.x = x

    def __eq__(self, other):
        return type(self) == type(other) and self.x == other.x  # pylint: disable=unidiomatic-typecheck

    @classmethod
    def fromconfig(cls, config):
        return cls(config["_x"])


@pytest.mark.parametrize(
    "config, expected",
    [
        pytest.param({"_attr_": "Custom", "_x": 1}, Custom(1), id="simple"),
        pytest.param(
            {"_attr_": "Config", "config": {"_attr_": "str", "_args_": "hello"}},
            fromconfig.Config(_attr_="str", _args_="hello"),
            id="config-with-attr",
        ),
    ],
)
def test_core_fromconfig(config, expected):
    """Test core.fromconfig."""
    assert fromconfig.fromconfig(config) == expected
