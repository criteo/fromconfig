"""Tests for utils.libimport."""

import functools

import pytest

import fromconfig


@pytest.mark.parametrize(
    "name, expected", [pytest.param("functools", functools), pytest.param("package_that_does_not_exist", None)]
)
def test_try_import(name, expected):
    """Test utils.try_import."""
    assert fromconfig.utils.try_import(name) == expected


class Class:
    """Class."""

    VARIABLE = "VARIABLE"

    def method(self):
        """Method."""


def function():
    """Gunction."""


@pytest.mark.parametrize(
    "name,expected",
    [
        pytest.param("", ImportError, id="empty"),
        pytest.param(".", ImportError, id="no-parts"),
        pytest.param("dict", dict, id="dict"),
        pytest.param("list", list, id="list"),
        pytest.param("function", function, id="local"),
        pytest.param("tests.unit.utils.test_utils_libimport.Class", Class, id="Class"),
        pytest.param("tests.unit.utils.test_utils_libimport.Class.method", Class.method, id="method"),
        pytest.param("tests.unit.utils.test_utils_libimport.Class.VARIABLE", Class.VARIABLE, id="VARIABLE"),
        pytest.param("tests.unit.utils.test_utils_libimport.function", function, id="function"),
        pytest.param("functools.partial", functools.partial, id="functools"),
    ],
)
def test_utils_from_import_string(name, expected):
    """Test utils.from_import_string."""
    if expected is ImportError:
        with pytest.raises(ImportError):
            fromconfig.utils.from_import_string(name)
    else:
        assert fromconfig.utils.from_import_string(name) == expected


@pytest.mark.parametrize(
    "attr,name",
    [
        pytest.param("A string", ValueError, id="string"),
        pytest.param(Class.VARIABLE, ValueError, id="VARIABLE"),
        pytest.param(fromconfig, "fromconfig", id="module"),
        pytest.param(str, "str", id="str"),
        pytest.param(dict, "dict", id="dict"),
        pytest.param(list, "list", id="list"),
        pytest.param(Class, "tests.unit.utils.test_utils_libimport.Class", id="Class"),
        pytest.param(Class.method, "tests.unit.utils.test_utils_libimport.Class.method", id="method"),
        pytest.param(function, "tests.unit.utils.test_utils_libimport.function", id="function"),
        pytest.param(functools.partial, "functools.partial", id="functools"),
        pytest.param(range(2), ValueError, id="generator"),
    ],
)
def test_utils_to_import_string(attr, name):
    """Test utils.to_import_string."""
    if name is ValueError:
        with pytest.raises(ValueError):
            fromconfig.utils.to_import_string(attr)
    else:
        assert fromconfig.utils.to_import_string(attr) == name
