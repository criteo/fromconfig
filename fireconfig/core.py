"""Core functionality."""

from abc import ABC
import functools
from typing import Dict
from enum import Enum
from fireconfig import utils


REF = "@"


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
        if isinstance(item, str) and item.startswith(REF):
            name = item[len(REF):]
            if name in references:
                return references[name]
            return item
        return item

    # If no cycle, no more than n - 1 edges to add
    for _ in range(len(references) - 1):
        config = utils.depth_map(_map_fn, config)

    return config


def assert_no_references(config: Dict):
    """Check that no more references in config."""
    references = utils.flatten_dict(config, lambda item: not any(key in item for key in Key))

    def _map_fn(item):
        if isinstance(item, str) and item.startswith(REF):
            name = item[len(REF):]
            if name in references:
                raise ValueError(f"Found reference {name} (check for cycles).")
        return item

    utils.depth_map(_map_fn, config)


def parse_config(config: Dict):
    """"Parse config by exploding kwargs and replacing references."""
    config = explode_kwargs(config)
    config = replace_references(config)
    assert_no_references(config)
    return config


def from_config(config):
    """Evaluate member."""
    if isinstance(config, dict):
        attribute = utils.string_import(config[Key.TYPE]) if Key.TYPE in config else dict
        if issubclass(attribute, FromConfig):
            return attribute.from_config({key: value for key, value in config.items() if key != Key.TYPE})
        args = from_config(config.get(Key.ARGS, ()))
        kwargs = {param: from_config(value) for param, value in config.items() if not any(key == param for key in Key)}
        init = Eval(config.get(Key.EVAL, Eval.CALL))
        if init == Eval.CALL:
            return attribute(*args, **kwargs)
        if init == Eval.PARTIAL:
            return functools.partial(attribute, *args, **kwargs)
        if init == Eval.IMPORT:
            if args:
                raise ValueError(f"Expected no args for {attribute} with {Key.EVAL} = {init}, but got {args}")
            if kwargs:
                raise ValueError(f"Expected no kwargs for {attribute} with {Key.EVAL} = {init}, but got {kwargs}")
            return attribute
        raise ValueError(f"{init} not supported")

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
