"""Utilities for testing."""


def assert_launcher_is_discovered(name: str, expected):
    """Test that a launcher is found by name."""
    # pylint: disable=import-outside-toplevel,cyclic-import
    from fromconfig.launcher.base import _get_cls

    assert _get_cls(name) is expected
