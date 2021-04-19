"""Tests for core.base."""

from typing import Dict

import pytest

import fromconfig


class Custom(fromconfig.FromConfig):
    """Custom FromConfig class."""

    def __init__(self, x):
        self.x = x

    def __eq__(self, other):
        return type(self) == type(other) and self.x == other.x  # pylint: disable=unidiomatic-typecheck


class CustomOverriden(Custom):
    """Custom FromConfig class with fromconfig implementation."""

    @classmethod
    def fromconfig(cls, config: Dict):
        return cls(config["_x"])


@pytest.mark.parametrize(
    "config, expected",
    [
        pytest.param({"x": 1}, Custom(1), id="simple"),
        pytest.param(
            {"x": {"_attr_": "tests.unit.core.test_core_base.Custom", "x": 2}}, Custom(Custom(2)), id="nested"
        ),
    ],
)
def test_default_custom_fromconfig(config, expected):
    """Test default custom fromconfig."""
    assert Custom.fromconfig(config) == expected


@pytest.mark.parametrize(
    "config, expected",
    [
        pytest.param(
            {"_attr_": "tests.unit.core.test_core_base.CustomOverriden", "_x": 1}, CustomOverriden(1), id="simple"
        ),
        pytest.param(
            {"_attr_": "fromconfig.Config", "_config_": {"_attr_": "str", "_args_": "hello"}},
            fromconfig.Config(_attr_="str", _args_="hello"),
            id="config-with-attr",
        ),
    ],
)
def test_core_fromconfig(config, expected):
    """Test core.fromconfig."""
    assert fromconfig.fromconfig(config) == expected
