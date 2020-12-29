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
        ("dict", dict),
        ("list", list),
        ("tests.unit.utils.test_utils_libimport.Class", Class),
        ("tests.unit.utils.test_utils_libimport.Class.method", Class.method),
        ("tests.unit.utils.test_utils_libimport.Class.VARIABLE", Class.VARIABLE),
        ("tests.unit.utils.test_utils_libimport.function", function),
        ("functools.partial", functools.partial)
    ],
)
def test_utils_import_from_string(name, expected):
    """Test utils.import_from_string."""
    assert fromconfig.utils.import_from_string(name) == expected
