"""Tests for utils.container."""

import pytest

import fromconfig


@pytest.mark.parametrize(
    "obj, expected",
    [
        pytest.param([], False, id="list"),
        pytest.param((), False, id="tuple"),
        pytest.param({}, True, id="dict"),
        pytest.param(fromconfig.Config(), True, id="Config"),
    ],
)
def test_utils_is_mapping(obj, expected):
    """Test utils.is_mapping."""
    assert fromconfig.utils.is_mapping(obj) == expected


@pytest.mark.parametrize(
    "obj, expected",
    [
        pytest.param([], True, id="list"),
        pytest.param({}, False, id="dict"),
        pytest.param("hello", False, id="string"),
        pytest.param((), True, id="tuple"),
    ],
)
def test_utils_is_pure_iterable(obj, expected):
    """Test utils.is_pure_iterable."""
    assert fromconfig.utils.is_pure_iterable(obj) == expected
