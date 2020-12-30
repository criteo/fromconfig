"""Tests for core.singleton."""

import pytest

import fromconfig


class Class:
    """Class."""


def test_core_singleton():
    """Test core.singleton."""
    x = fromconfig.singleton("singleton", Class)
    y = fromconfig.singleton("singleton", Class)
    z = fromconfig.singleton("singleton")
    assert id(x) == id(y) == id(z)


def test_core_singleton_missing_constructor():
    """Test core.singleton missing constructor."""
    with pytest.raises(ValueError):
        fromconfig.singleton("missing_singleton")
