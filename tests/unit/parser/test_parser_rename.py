"""Test for parser.rename."""

import fromconfig


def test_parser_rename():
    """Test parser.RenameParser."""
    parser = fromconfig.parser.RenameParser({"x": "y"})
    parsed = parser({"x": 1})
    assert parsed == {"y": 1}
