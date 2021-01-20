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


class Update(fromconfig.parser.Parser):
    """Update parser."""

    def __init__(self, update: Mapping):
        self.update = update

    def __call__(self, config: Mapping):
        return {**config, **self.update}


def test_parser_chain():
    """Test parser.Chain."""
    parser = fromconfig.parser.Chain(Update({1: 2}), Update({3: 4}))
    parsed = parser({})
    assert parsed == {1: 2, 3: 4}
