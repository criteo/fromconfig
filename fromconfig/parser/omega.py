"""Simple OmegaConf parser."""

from typing import Mapping, Dict, Union, Callable
from datetime import datetime
from functools import partial

from omegaconf import OmegaConf

from fromconfig.core.base import fromconfig
from fromconfig.parser import base
from fromconfig.utils.libimport import from_import_string
from fromconfig.utils.types import is_mapping


@partial(OmegaConf.register_resolver, "now")
def now(fmt: str = "%Y-%m-%d-%H-%M-%S") -> str:
    return datetime.now().strftime(fmt)


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
    >>> config = {"hello_world": "${hello:world}", "date": "${now:}"}
    >>> parser = fromconfig.parser.OmegaConfParser({"hello": "hello"})
    >>> parsed = parser(config)
    >>> assert parsed["hello_world"] == "hello world"  # Custom resolver
    >>> assert "$" not in parsed["date"]  # Make sure now was resolved
    """

    def __init__(self, resolvers: Dict[str, Union[str, Dict, Callable]] = None):
        # Register custom resolvers
        if resolvers:
            for name, resolver in resolvers.items():
                if isinstance(resolver, str):
                    resolver = from_import_string(resolver)
                elif is_mapping(resolver):
                    resolver = fromconfig(resolver)
                elif callable(resolver):
                    pass
                else:
                    raise TypeError(f"Unable to resolve {resolver}")
                OmegaConf.register_resolver(name, resolver)

    def __call__(self, config: Mapping) -> Mapping:
        # Create and resolve config
        conf = OmegaConf.create(config)  # type: ignore
        return OmegaConf.to_container(conf, resolve=True)  # type: ignore
