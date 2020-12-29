"""Tests for core.singleton."""

import fromconfig


class Class:
    """Class."""


def test_core_singleton():
    """Test core.singleton."""
    x = fromconfig.singleton("singleton", Class)
    y = fromconfig.singleton("singleton", Class)
    z = fromconfig.singleton("singleton")
    assert id(x) == id(y) == id(z)
