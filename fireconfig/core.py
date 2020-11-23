"""Core functionality."""

from abc import ABC, abstractclassmethod
import functools
from typing import Dict
from enum import Enum
from fireconfig.utils import child_map, import_string, flatten_dict


class FromConfig(ABC):

    @abstractclassmethod
    def from_config(cls, config: Dict):
        raise NotImplementedError()


class Config(dict, FromConfig):
    """Simple wrapper for config dictionaries."""

    def __init__(self, config: Dict):
        if not isinstance(config, dict):
            raise TypeError(f"Config expected a dict but got {config}")
        super().__init__(**config)

    @classmethod
    def from_config(cls, config: Dict):
        return cls(config=config)


_SINGLETONS = {}


def singleton(key, constructor):
    if key not in _SINGLETONS:
        _SINGLETONS[key] = constructor()
    return _SINGLETONS[key]


class Key(str, Enum):
    """Key."""

    EVAL = "eval"
    TYPE = "type"
    PARSE = "parse"
    KWARGS = "**"
    ARGS = "*"


class Eval(str, Enum):
    """Eval."""

    CALL = "call"
    PARTIAL = "partial"
    IMPORT = "import"

    def call(self, attr, *args, **kwargs):
        """Evaluate attribute with args and kwargs."""
        if self == self.CALL:
            return attr(*args, **kwargs)
        if self == self.PARTIAL:
            return functools.partial(attr, *args, **kwargs)
        if self == self.IMPORT:
            if args:
                raise ValueError(f"Expected no args for {attr} but got {args}")
            if kwargs:
                raise ValueError(f"Expected no kwargs for {attr} but got {kwargs}")
            return attr
        raise ValueError(self)


def explode_kwargs(config: Dict):
    kwargs = config.get(Key.KWARGS, {})
    if not isinstance(kwargs, dict):
        raise TypeError(f"Expected type dict for key {Key.KWARGS} but got {type(kwargs)} (item = {config})")
    for key, value in config.items():
        if key != Key.KWARGS:
            kwargs[key] = value
    return kwargs


def evaluate(config):
    """Evaluate member."""
    if isinstance(config, dict):
        args = config.get(Key.ARGS, ())
        kwargs = config.get(Key.KWARGS, {})
        kwargs.update({param: value for param, value in config.items() if not any(key == param for key in Key)})
        if Key.TYPE in config:
            return Eval(config.get(Key.EVAL, Eval.CALL)).call(import_string(config[Key.TYPE]), *args, **kwargs)
        if args:
            raise ValueError(f"Got simple dictionary with protected key {Key.ARGS} ({config})")
        return kwargs
    return config


def reference(item):
    if isinstance(item, str) and item.startswith("@"):
        return item[1:]
    return None


def from_config(config: Dict):
    """"Instantiate object from config.

    - move kwargs one level up
    - extract references
    - replace references
    - evaluate
    """
    return (
        Config(config)
        .explode_kwargs()
        .replace_references()
        .evaluate()
    )
    config = child_map(lambda item: explode_kwargs(item) if isinstance(item, dict) else item, config)
    references = flatten_dict(config, lambda item: not any(key in item for key in Key))
    for _ in range(len(references) - 1):
        config = child_map(lambda item: references.get(reference(item), item) if reference(item) else item, config)
    return child_map(evaluate, config)
