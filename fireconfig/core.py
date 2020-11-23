"""Core functionality."""

from abc import ABC
import collections
import functools
from typing import Dict
from enum import Enum
from fireconfig import utils


class Key(str, Enum):
    """Special dictionary keys reserved for the config system."""

    TYPE = "type"
    EVAL = "eval"
    ARGS = "*"
    KWARGS = "**"


class Eval(str, Enum):
    """Different evaluation modes given a config dictionary."""

    CALL = "call"
    PARTIAL = "partial"
    IMPORT = "import"


class Reference(collections.UserString):
    """Normalize reference strings."""

    PREFIX = "@"

    def __init__(self, data):
        if not data.startswith(self.PREFIX):
            raise ValueError(f"{data} is not a proper reference (no prefix {self.PREFIX})")
        super().__init__(data[len(self.PREFIX):])

    @classmethod
    def is_valid(cls, value) -> bool:
        return isinstance(value, str) and value.startswith(cls.PREFIX)


class FromConfig(ABC):
    """Abstract class for custom from_config implementations."""

    @classmethod
    def from_config(cls, config: Dict):
        raise NotImplementedError()


def explode_kwargs(config: Dict):
    """Explode kwargs key in config and its children."""

    def _map_fn(item):
        if isinstance(item, dict) and Key.KWARGS in item:
            kwargs = item[Key.KWARGS]
            if not isinstance(kwargs, dict):
                raise TypeError(f"Expected type dict for key {Key.KWARGS} but got {type(kwargs)} (item = {item})")
            # Keys at top-level override kwargs keys
            for key, value in item.items():
                if key != Key.KWARGS:
                    kwargs[key] = value
            return kwargs
        return item

    return utils.depth_map(_map_fn, config)


def replace_references(config: Dict):
    """Replace references in config and its children."""
    references = utils.flatten_dict(config, lambda item: not any(key in item for key in Key))

    def _map_fn(item):
        if Reference.is_valid(item):
            if Reference(item) in references:
                return references[Reference(item)]
            return item
        return item

    # If no cycle, no more than n - 1 edges to add
    # TODO: more deterministic? (resolve order, check no cycle)
    for _ in range(len(references) - 1):
        config = utils.depth_map(_map_fn, config)

    return config


def assert_no_references(config: Dict):
    """Check that no more references in config."""
    references = utils.flatten_dict(config, lambda item: not any(key in item for key in Key))

    def _map_fn(item):
        if Reference.is_valid(item):
            # TODO: @params.x if x not in params does not fail
            if Reference(item) in references:
                raise ValueError(f"Found reference {item} (check for cycles).")
        return item

    utils.depth_map(_map_fn, config)


def parse_config(config: Dict):
    """"Parse config by exploding kwargs and replacing references."""
    config = explode_kwargs(config)
    config = replace_references(config)
    assert_no_references(config)
    # TODO: special case of @self @macro etc.?
    return config


def from_config(config):
    """Evaluate member."""
    if isinstance(config, dict):
        attribute = utils.string_import(config[Key.TYPE]) if Key.TYPE in config else dict
        if issubclass(attribute, FromConfig):
            return attribute.from_config({key: value for key, value in config.items() if key != Key.TYPE})
        args = from_config(config.get(Key.ARGS, ()))
        kwargs = {param: from_config(value) for param, value in config.items() if not any(key == param for key in Key)}
        mode = Eval(config.get(Key.EVAL, Eval.CALL))
        if mode == Eval.CALL:
            return attribute(*args, **kwargs)
        if mode == Eval.PARTIAL:
            return functools.partial(attribute, *args, **kwargs)
        if mode == Eval.IMPORT:
            if args:
                raise ValueError(f"Expected no args for {attribute} with {Key.EVAL} = {mode}, but got {args}")
            if kwargs:
                raise ValueError(f"Expected no kwargs for {attribute} with {Key.EVAL} = {mode}, but got {kwargs}")
            return attribute
        raise ValueError(f"{mode} not supported")

    if isinstance(config, tuple):
        return tuple(from_config(it) for it in config)
    if isinstance(config, list):
        return list(from_config(it) for it in config)
    return config


# TODO: syntactic sugar for Config / Singletons?
# TODO: should singleton really belong to the config library?


class Config(dict, FromConfig):
    """Avoid recursive evaluation on config objects."""

    @classmethod
    def from_config(cls, config: Dict):
        return cls(**config["config"])


_SINGLETONS = {}


def singleton(key, constructor):
    if key not in _SINGLETONS:
        _SINGLETONS[key] = constructor()
    return _SINGLETONS[key]
