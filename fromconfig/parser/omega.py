"""Simple OmegaConf parser."""

from typing import Any
from datetime import datetime

from omegaconf import OmegaConf

from fromconfig.core.base import fromconfig
from fromconfig.parser import base
from fromconfig.utils.libimport import from_import_string
from fromconfig.utils.types import is_mapping, is_pure_iterable
from fromconfig.utils.nest import merge_dict


def now(fmt: str = "%Y-%m-%d-%H-%M-%S") -> str:
    return datetime.now().strftime(fmt)


_RESOLVERS = {"now": now}  # Default Resolvers


class OmegaConfParser(base.Parser):
    """Simple OmegaConf parser.

    Example
    -------
    >>> import fromconfig
    >>> config = {
    ...     "host": "localhost",
    ...     "port": "8008",
    ...     "url": "${host}:${port}"
    ... }
    >>> parser = fromconfig.parser.OmegaConfParser()
    >>> parsed = parser(config)
    >>> parsed["url"]
    'localhost:8008'

    You can configure custom resolvers for custom variable
    interpolation. For example

    >>> import fromconfig
    >>> def hello(s):
    ...     return f"hello {s}"
    >>> config = {
    ...     "hello_world": "${hello:world}",
    ...     "date": "${now:}",
    ...     "resolvers": {"hello": "hello"}
    ... }
    >>> parser = fromconfig.parser.OmegaConfParser()
    >>> parsed = parser(config)
    >>> assert parsed["hello_world"] == "hello world"  # Custom resolver
    >>> assert "$" not in parsed["date"]  # Make sure now was resolved
    """

    def __call__(self, config: Any) -> Any:
        # Extract resolvers to register
        if is_mapping(config):
            resolvers = merge_dict(_RESOLVERS, config.get("resolvers") or {})
            config = {key: value for key, value in config.items() if key != "resolvers"}
        else:
            resolvers = _RESOLVERS

        # Register resolvers
        for name, resolver in resolvers.items():
            if isinstance(resolver, str):
                resolver = from_import_string(resolver)
            elif is_mapping(resolver):
                resolver = fromconfig(resolver)
            elif callable(resolver):
                pass
            else:
                raise TypeError(f"Unable to resolve {resolver}")
            OmegaConf.register_new_resolver(name, resolver)

        # Create config and parse
        if is_mapping(config) or is_pure_iterable(config):
            conf = OmegaConf.create(config)  # type: ignore
            parsed = OmegaConf.to_container(conf, resolve=True)  # type: ignore
        else:
            # Try to parse by wrapping in a list
            conf = OmegaConf.create([config])  # type: ignore
            parsed = OmegaConf.to_container(conf, resolve=True)[0]  # type: ignore

        # Clear resolvers (avoid leaking module-level changes), return
        OmegaConf.clear_resolvers()
        return parsed
