"""Tests for utils.libimport."""

import functools

import pytest

import fromconfig


class Class:
    """Class."""

    VARIABLE = "VARIABLE"

    def method(self):
        """Method."""


def function():
    """function."""


@pytest.mark.parametrize(
    "name,expected",
    [
        pytest.param("dict", dict, id="dict"),
        pytest.param("list", list, id="list"),
        pytest.param("tests.unit.utils.test_utils_libimport.Class", Class, id="Class"),
        pytest.param("tests.unit.utils.test_utils_libimport.Class.method", Class.method, id="method"),
        pytest.param("tests.unit.utils.test_utils_libimport.Class.VARIABLE", Class.VARIABLE, id="VARIABLE"),
        pytest.param("tests.unit.utils.test_utils_libimport.function", function, id="function"),
        pytest.param("functools.partial", functools.partial, id="functools"),
    ],
)
def test_utils_import_from_string(name, expected):
    """Test utils.import_from_string."""
    assert fromconfig.utils.import_from_string(name) == expected
