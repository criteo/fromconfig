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
        pytest.param("missing_function", Exception, id="missing"),
    ],
)
@pytest.mark.parametrize("safe", [True, False])
def test_core_register(name, expected, safe):
    """Test core.register."""
    if expected is Exception:
        with pytest.raises(Exception):
            fromconfig.register.resolve(name, safe=safe)
    else:
        assert fromconfig.register.resolve(name, safe=safe) == expected
