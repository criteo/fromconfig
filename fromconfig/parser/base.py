"""Base functionality for parsers."""

from abc import ABC, abstractmethod
from typing import Callable, Mapping


class Parser(ABC):
    """Base parser class."""

    @abstractmethod
    def __call__(self, config: Mapping):
        raise NotImplementedError()


class Chain(Parser):
    """Chain parsers."""

    def __init__(self, *parsers: Callable):
        self.parsers = parsers

    def __call__(self, config: Mapping):
        for parser in self.parsers:
            config = parser(config)
        return config
