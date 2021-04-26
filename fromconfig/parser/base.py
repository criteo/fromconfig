"""Base functionality for parsers."""

from abc import ABC, abstractmethod
from typing import Any


class Parser(ABC):
    """Base parser class."""

    @abstractmethod
    def __call__(self, config: Any):
        raise NotImplementedError()


class ChainParser(Parser):
    """A parser that applies parsers sequentially."""

    def __init__(self, *parsers: Parser):
        self.parsers = parsers

    def __call__(self, config: Any):
        parsed = config
        for parser in self:
            parsed = parser(parsed)
        return parsed

    def __iter__(self):
        return iter(self.parsers)

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(map(repr, self))})"
