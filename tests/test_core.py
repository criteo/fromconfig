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
        "a": 0,
        "b": 1,
        "**": {
            "c": 2
        }
    },
    "params": {
        "a": "@constants.a",
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
            "type": "fireconfig.core.Config",
            "config": {
                "type": "some.module"
            }
        }
    }
}


def test_from_config():
    print(core.from_config(core.parse_config({**config, **core.from_config(core.parse_config(macros))})))
