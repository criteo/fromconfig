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


@pytest.mark.parametrize(
    "name,expected",
    [
        pytest.param("Class", Class, id="class"),
        pytest.param("Class.method", Class.method, id="method"),
        pytest.param("function", function, id="function"),
    ],
)
@pytest.mark.parametrize("safe", [True, False])
def test_core_register(name, expected, safe):
    """Test core.register."""
    assert fromconfig.register.resolve(name, safe=safe) == expected
