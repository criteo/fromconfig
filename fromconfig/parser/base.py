"""Base functionality for parsers."""

from abc import ABC, abstractmethod
from typing import Mapping


class Parser(ABC):
    """Base parser class."""

    @abstractmethod
    def __call__(self, config: Mapping):
        raise NotImplementedError()
