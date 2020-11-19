"""Tests for core."""

import dataclasses
from fireconfig import core
from typing import Dict


@dataclasses.dataclass
class A:
    a: float


@dataclasses.dataclass
class B:
    b: A
    c: Dict


config = {
    "params": {
        "learning_rate": 0.1
    },
    "a": {
        "type": "test_core.A",
        "a": "@params.learning_rate"
    },
    "main": {
        "type": "test_core.B",
        "b": "@a",
        "c": {
            "parse": "dict",
            "e": {
                "type": "test_core.A",
                "a": "@params.learning_rate"
            }
        }
    }
}


def test_from_config():
    print(core.from_config(config)["main"])
