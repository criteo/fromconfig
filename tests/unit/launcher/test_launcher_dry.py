"""Test launcher.dry."""

import fromconfig


def test_launcher_dry():
    """Test dry launcher."""
    launcher = fromconfig.launcher.DryLauncher()
    launcher({"foo": "bar"}, "foo")
