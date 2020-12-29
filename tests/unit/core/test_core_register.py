"""Tests for core.register."""

import pytest

import fromconfig


@fromconfig.register("Class")
class Class:
    """Class."""

    VARIABLE = "VARIABLE"

    @fromconfig.register("Class.method")
    def method(self):
        """Method."""


@fromconfig.register("function")
def function():
    """function."""


@pytest.mark.parametrize("name,expected", [("Class", Class), ("Class.method", Class.method), ("function", function)])
@pytest.mark.parametrize("safe", [True, False])
def test_core_register(name, expected, safe):
    """Test core.register."""
    assert fromconfig.register.resolve(name, safe=safe) == expected
