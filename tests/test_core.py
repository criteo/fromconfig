"""Tests for core."""

from typing import Dict
import dataclasses
from fireconfig import core


@dataclasses.dataclass
class A:
    a: float
    b: float
    c: Dict

    def __repr__(self):
        return f"A(a={self.a}, b={self.b}, c={self.c}, id={id(self)})"


class Macro(dict):
    """Macro."""


macros = {
    "constants": {
        "b": 0
    },
    "params": {
        "a": 1,
        "**": {
            "type": "test_core.Macro",
            "b": "@constants.b"
        }
    }
}
config = {
    "main": {
        "type": "test_core.A",
        "eval": "call",
        "a": "@params.a",
        "b": "@params.b",
        "c": {
            "type": "some.module",
            "parse": "dict",
        }
    }
}


def test_from_config():
    print(core.from_config({**config, **core.from_config(macros)}))
