"""Config serialization utilities."""

from pathlib import Path
from typing import Union, Mapping, Any, IO
import json
import logging
import os

import yaml

from fromconfig.core import base
from fromconfig.utils import try_import


_jsonnet = try_import("_jsonnet")


LOGGER = logging.getLogger(__name__)


class Config(base.FromConfig, dict):
    """Keep a dictionary as dict during a fromconfig call.

    Example
    -------
    >>> import fromconfig
    >>> config = {
    ...     "_attr_": "fromconfig.Config",
    ...     "_config_": {
    ...         "_attr_": "list"
    ...     }
    ... }
    >>> parsed = fromconfig.fromconfig(config)
    >>> parsed
    {'_attr_': 'list'}
    """

    @classmethod
    def fromconfig(cls, config: Mapping):
        return cls(config.get("_config_", config))


class Loader(yaml.SafeLoader):
    """YAML Loader with `!include` constructor."""

    def __init__(self, stream: IO) -> None:
        """Initialize Loader."""
        try:
            self._root = os.path.split(stream.name)[0]
        except AttributeError:
            self._root = os.path.curdir
        super().__init__(stream)


def construct_include(loader: Loader, node: yaml.Node) -> Any:
    """Include file referenced at node."""
    # pylint: disable=protected-access
    filename = os.path.abspath(os.path.join(loader._root, loader.construct_scalar(node)))
    extension = os.path.splitext(filename)[1].lstrip(".")
    with open(filename, "r") as f:
        if extension in ("yaml", "yml"):
            return yaml.load(f, Loader)
        elif extension in ("json",):
            return json.load(f)
        else:
            return "".join(f.readlines())


yaml.add_constructor("!include", construct_include, Loader)


def load(path: Union[str, Path]):
    """Load dictionary from path.

    Parameters
    ----------
    path : Union[str, Path]
        Path to file (yaml, yml, json or jsonnet format)
    """
    suffix = Path(path).suffix
    if suffix in (".yaml", ".yml"):
        with Path(path).open() as file:
            return yaml.load(file, Loader)
    if suffix == ".json":
        with Path(path).open() as file:
            return json.load(file)
    if suffix == ".jsonnet":
        if _jsonnet is None:
            msg = f"jsonnet is not installed but the resolved path extension is {suffix}. "
            msg += "Visit https://jsonnet.org for installation instructions."
            raise ImportError(msg)
        return json.loads(_jsonnet.evaluate_file(str(path)))
    raise ValueError(f"Unable to resolve method for path {path}")


def dump(config, path: Union[str, Path]):
    """Dump dictionary content to file in path.

    Parameters
    ----------
    path : Union[str, Path]
        Path to file (yaml, yml, json or jsonnet format)
    """
    suffix = Path(path).suffix
    if suffix in (".yaml", ".yml"):
        with Path(path).open("w") as file:
            yaml.dump(config, file)
    elif suffix in (".json", ".jsonnet"):
        with Path(path).open("w") as file:
            json.dump(config, file)
    else:
        raise ValueError(f"Suffix {suffix} not recognized for path {path}")
