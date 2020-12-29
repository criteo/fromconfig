"""Test for parser.base."""

from typing import Mapping

import fromconfig


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


def test_parser_select():
    """Test parser.Select."""
    parser = fromconfig.parser.Select(key="x", parser=Update({1: 2}))
    parsed = parser({"x": {}, "y": {3: 4}})
    assert parsed == {"x": {1: 2}, "y": {3: 4}}
