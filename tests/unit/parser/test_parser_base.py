"""Test for parser.base."""

from typing import Mapping

import pytest

import fromconfig


def test_parser_parser_class_is_abstract():
    """Test that from config is abstract."""
    with pytest.raises(Exception):
        fromconfig.parser.Parser()  # pylint: disable=abstract-class-instantiated

    with pytest.raises(NotImplementedError):
        fromconfig.parser.Parser.__call__(None, {"x": 1})
