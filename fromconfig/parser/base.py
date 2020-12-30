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


class Select(Parser):
    """Apply parser only on one key."""

    def __init__(self, key: str, parser: Callable):
        self.key = key
        self.parser = parser

    def __call__(self, config: Mapping):
        if self.key in config:
            parsed = self.parser(config[self.key])
            return {self.key: parsed, **{key: value for key, value in config.items() if key != self.key}}
        return config
