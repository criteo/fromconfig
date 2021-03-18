"""Evaluate parser."""

from typing import Mapping
import functools
import logging

from fromconfig.core import Keys
from fromconfig.parser import base
from fromconfig.utils import StrEnum, depth_map, is_mapping, to_import_string, from_import_string


LOGGER = logging.getLogger(__name__)


class EvaluateMode(StrEnum):
    """Evaluation modes."""

    CALL = "call"
    PARTIAL = "partial"
    IMPORT = "import"


class EvaluateParser(base.Parser):
    """Evaluate parser.

    Examples
    --------
    Mode "call"
    >>> import fromconfig
    >>> config = {"_attr_": "str", "_eval_": "call", "_args_": ["hello world"]}
    >>> parser = fromconfig.parser.EvaluateParser()
    >>> parsed = parser(config)
    >>> fromconfig.fromconfig(parsed) == "hello world"
    True

    Mode "partial"
    >>> import fromconfig
    >>> config = {"_attr_": "str", "_eval_": "partial", "_args_": ["hello world"]}
    >>> parser = fromconfig.parser.EvaluateParser()
    >>> parsed = parser(config)
    >>> fn = fromconfig.fromconfig(parsed)
    >>> isinstance(fn, functools.partial)
    True
    >>> fn() == "hello world"
    True

    Mode "import"
    >>> import fromconfig
    >>> config = {"_attr_": "str", "_eval_": "import"}
    >>> parser = fromconfig.parser.EvaluateParser()
    >>> parsed = parser(config)
    >>> fromconfig.fromconfig(parsed) is str
    True
    """

    KEY = "_eval_"

    def __call__(self, config: Mapping):
        """Parses configs with _eval_ key into valid config."""

        def _map_fn(item):
            if is_mapping(item) and self.KEY in item:
                # Get mode, attribute name, args, and kwargs from item
                evaluate = EvaluateMode(item[self.KEY])
                name = item[Keys.ATTR]
                args = item.get(Keys.ARGS, [])
                kwargs = {key: value for key, value in item.items() if key not in (self.KEY, Keys.ATTR, Keys.ARGS)}

                # If IMPORT, should just import the attribute
                if evaluate == EvaluateMode.IMPORT:
                    if args or kwargs:
                        msg = f"Found {args} {kwargs} in item {item}, expected only {Keys.ATTR} (evaluate = {evaluate})"
                        raise ValueError(msg)
                    return {Keys.ATTR.value: to_import_string(from_import_string), Keys.ARGS.value: [name]}

                # If PARTIAL, wrap type (if present)
                if evaluate == EvaluateMode.PARTIAL:
                    fn = {Keys.ATTR.value: to_import_string(from_import_string), "name": name}
                    return {
                        Keys.ATTR.value: to_import_string(functools.partial),
                        Keys.ARGS.value: [fn, *args],
                        **kwargs,
                    }

                # If CALL, nothing to do (default behavior)
                if evaluate == EvaluateMode.CALL:
                    return {Keys.ATTR.value: name, Keys.ARGS.value: args, **kwargs}

            return item

        return depth_map(_map_fn, config)
