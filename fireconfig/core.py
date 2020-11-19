"""Core functionality."""

import functools
from typing import Dict
from enum import Enum
from fireconfig.utils import child_map, import_from_string, flatten_dict


class SpecialKey(Enum):
    """Special Keys."""

    PARSE = "parse"
    EVAL = "eval"
    TYPE = "type"
    POSITIONAL = "*"

    @classmethod
    def is_in(cls, item):
        return any(key.value in item for key in cls)


class ParseMode(Enum):
    """Parse mode."""

    DICT = "dict"
    INIT = "init"

    def parse(self, item: Dict):
        item = {key: value for key, value in item.items() if key != SpecialKey.PARSE.value}
        if self is self.DICT:
            return item
        if self is self.INIT:
            return evaluate(item)
        raise ValueError(f"No evaluation defined for {self}")


class EvalMode(Enum):
    """Evaluation Types."""

    CALL = "call"
    PARTIAL = "partial"
    IMPORT = "import"

    def evaluate(self, item: Dict):
        """Evaluate item."""
        member = import_from_string(item[SpecialKey.TYPE.value])
        if self is self.IMPORT:
            return member
        args = item.get(SpecialKey.POSITIONAL.value, ())
        kwargs = {key: value for key, value in item.items() if not SpecialKey.is_in([key])}
        if self is self.PARTIAL:
            return functools.partial(member, *args, **kwargs)
        if self is self.CALL or self is self.SINGLETON:
            return member(*args, **kwargs)
        raise ValueError(f"No initialization defined for {self}")


def evaluate(item):
    if isinstance(item, dict) and SpecialKey.TYPE.value in item:
        eval_mode = EvalMode(item.get(SpecialKey.EVAL.value, "call"))
        return eval_mode.evaluate(item)
    return item


def parse(item):
    if isinstance(item, dict):
        parse_mode = ParseMode(item.get(SpecialKey.PARSE.value, "init"))
        return parse_mode.parse(item)
    return item


def reference(item):
    if isinstance(item, str) and item.startswith("@"):
        return item[1:]
    return None


def from_config(config: Dict):
    """"Instantiate object from config."""
    config = flatten_dict(config, lambda item: not SpecialKey.is_in(item))
    for _ in range(len(config) - 1):
        config = child_map(lambda item: config.get(reference(item), item), config)
    return child_map(
        parse,
        config,
        lambda item: isinstance(item, dict) and item.get(SpecialKey.PARSE.value) == ParseMode.DICT.value
    )
