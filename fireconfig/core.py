"""Core functionality."""

import functools
from typing import Dict
from enum import Enum
from fireconfig.utils import child_map, import_from_string, flatten_dict


class Key(str, Enum):
    """Key."""

    EVAL = "eval"
    TYPE = "type"
    PARSE = "parse"
    KWARGS = "**"
    ARGS = "*"


class Parse(str, Enum):
    """Parse."""

    DICT = "dict"
    EVAL = "eval"


class Eval(str, Enum):
    """Eval."""

    CALL = "call"
    PARTIAL = "partial"
    IMPORT = "import"

    @classmethod
    def evaluate(cls, config):
        """Evaluate member."""
        if isinstance(config, dict) and Key.TYPE in config:
            mode = Eval(config.get(Key.EVAL, Eval.CALL))
            member = import_from_string(config[Key.TYPE])
            args = config.get(Key.ARGS, ())
            kwargs = {param: value for param, value in config.items() if not any(key == param for key in Key)}
            if mode == cls.CALL:
                return member(*args, **kwargs)
            if mode == cls.PARTIAL:
                return functools.partial(member, *args, **kwargs)
            if mode == cls.IMPORT:
                if args:
                    raise ValueError(f"Expected no args for {member} but got {args}")
                if kwargs:
                    raise ValueError(f"Expected no kwargs for {member} but got {kwargs}")
                return member
            raise ValueError(mode)
        return config


def reference(item):
    if isinstance(item, str) and item.startswith("@"):
        return item[1:]
    return None


_SINGLETONS = {}


def singleton(key, constructor):
    if key not in _SINGLETONS:
        _SINGLETONS[key] = constructor()
    return _SINGLETONS[key]


def parse(item):
    if isinstance(item, dict) and isinstance(item.get(Key.KWARGS), dict):
        return {**item[Key.KWARGS], **{key: value for key, value in item.items() if key != Key.KWARGS}}
    return item


def from_config(config: Dict):
    """"Instantiate object from config."""
    config = child_map(parse, config)
    references = flatten_dict(config, lambda item: not any(key in item for key in Key))
    for _ in range(len(references) - 1):
        config = child_map(lambda item: references.get(reference(item), item) if reference(item) else item, config)
    return child_map(Eval.evaluate, config, lambda item: isinstance(item, dict) and item.get(Key.PARSE) == Parse.DICT)
