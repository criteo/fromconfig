"""Evaluate parser."""
from typing import Any, Callable, List, Dict
import functools
import logging

from fromconfig.core import Keys
from fromconfig.parser import base
from fromconfig.parser.singleton import _Singletons
from fromconfig.utils import StrEnum, depth_map, is_mapping, to_import_string, from_import_string


LOGGER = logging.getLogger(__name__)


class EvaluateMode(StrEnum):
    """Evaluation modes."""

    CALL = "call"
    PARTIAL = "partial"
    IMPORT = "import"
    LAZY = "lazy"


_lazy_arg_singleton = _Singletons()


class _LazyArg:
    """A class used to represent a lazy argument.

    ...

    Attributes
    ----------
    constructor: Callable
        The constructor to call.
    memoization_key: str
        The key to use for memoization. If None, there is no memoization.
    args: List[Any]
        The positional arguments to pass to the constructor.
    kwargs: Dict[str, Any]
        The keyword arguments to pass to the constructor.
    """

    def __init__(self, constructor: Callable, memoization_key: str, *args, **kwargs):
        self.constructor = constructor
        self.memoization_key = memoization_key
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        if self.memoization_key is None:
            return self.constructor(*self.args, **self.kwargs)
        else:
            self_contained_constructor = functools.partial(self.constructor, *self.args, **self.kwargs)
            return _lazy_arg_singleton(self.memoization_key, self_contained_constructor)


def _fn_with_lazy_instantiations_constructor(
    fn: Callable, lazy_args_mask: List[bool], lazy_kwargs_map: Dict[str, bool]
):
    """Returns a function that instantiates lazy arguments after the function is called.

    If fn is a callable and its arguments have types T1, T2, ...
    then _fn_with_lazy_instantiations_constructor returns a callable
    with a semantic similar to fn but its arguments have types T'1, T'2, ...
    where T'i is
     - Ti is the argument is not lazy (unchanged)
     - Callable[[], Ti] if the argument is lazy
     Lazy arguments are evaluated when the new callable is called and then fn is called with all evaluated arguments
    """

    def _fn_with_lazy_instantiations(*args, **kwargs):
        padded_lazy_args_mask = lazy_args_mask + [False] * (len(args) - len(lazy_args_mask))
        evaluated_args = [arg() if is_lazy else arg for arg, is_lazy in zip(args, padded_lazy_args_mask)]
        evaluated_kwargs = {key: value() if lazy_kwargs_map.get(key) else value for key, value in kwargs.items()}
        return fn(*evaluated_args, **evaluated_kwargs)

    return _fn_with_lazy_instantiations


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

    Mode "lazy"
    >>> import fromconfig
    >>> trackable_str = lambda s: print("In trackable_str") or s
    >>> config = {
    ...     "_attr_": "str",
    ...     "_eval_": "partial",
    ...     "_args_": [{"_attr_": "trackable_str", "_args_": ["hello world"], "_eval_": "lazy"}]
    ... }
    >>> parser = fromconfig.parser.EvaluateParser()
    >>> parsed = parser(config)
    >>> fn = fromconfig.fromconfig(parsed)
    >>> # Note that `trackable_str` has not been called yet
    >>> output = fn()
    In trackable_str
    >>> output == "hello world"
    True
    """

    KEY = "_eval_"
    MEMOIZATION_KEY = "_memoization_key_"

    def __call__(self, config: Any):
        """Parses configs with _eval_ key into valid config."""

        def _map_fn(item):
            if is_mapping(item) and self.KEY in item:
                # Get mode, attribute name, args, and kwargs from item
                evaluate = EvaluateMode(item[self.KEY])
                name = item[Keys.ATTR]
                args = item.get(Keys.ARGS, [])
                kwargs = {
                    key: value
                    for key, value in item.items()
                    if key not in (self.KEY, self.MEMOIZATION_KEY, Keys.ATTR, Keys.ARGS)
                }

                # If IMPORT, should just import the attribute
                if evaluate == EvaluateMode.IMPORT:
                    if args or kwargs:
                        msg = f"Found {args} {kwargs} in item {item}, expected only {Keys.ATTR} (evaluate = {evaluate})"
                        raise ValueError(msg)
                    return {Keys.ATTR.value: to_import_string(from_import_string), Keys.ARGS.value: [name]}

                # If LAZY, wrap into a _LazyArg
                if evaluate == EvaluateMode.LAZY:
                    fn = {Keys.ATTR.value: to_import_string(from_import_string), "name": name}
                    key = item.get(self.MEMOIZATION_KEY)
                    output = {
                        Keys.ATTR.value: to_import_string(_LazyArg),
                        Keys.ARGS.value: [fn, key, *args],
                        **kwargs,
                    }
                    return output

                # If PARTIAL, wrap type (if present)
                if evaluate == EvaluateMode.PARTIAL:

                    def is_lazy(arg):
                        return bool(is_mapping(arg) and arg[Keys.ATTR.value] == to_import_string(_LazyArg))

                    lazy_args_mask = [is_lazy(arg) for arg in args]
                    lazy_kwargs_map = {key: is_lazy(value) for key, value in kwargs.items()}

                    has_lazy_args_or_kwargs = any(lazy_args_mask) or any(lazy_kwargs_map.values())

                    if not has_lazy_args_or_kwargs:
                        fn = {Keys.ATTR.value: to_import_string(from_import_string), "name": name}
                    else:
                        fn = {
                            Keys.ATTR.value: to_import_string(_fn_with_lazy_instantiations_constructor),
                            "fn": {Keys.ATTR.value: to_import_string(from_import_string), "name": name},
                            "lazy_args_mask": lazy_args_mask,
                            "lazy_kwargs_map": lazy_kwargs_map,
                        }
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
