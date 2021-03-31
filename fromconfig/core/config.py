"""Config serialization utilities."""

from pathlib import Path
from typing import Union, Mapping
import json
import logging

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
            return yaml.safe_load(file)
    if suffix == ".json":
        with Path(path).open() as file:
            return json.load(file)
    if suffix == ".jsonnet":
        if _jsonnet is None:
            raise ImportError("Unable to import _jsonnet.")
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
