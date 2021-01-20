"""Config Class."""

from collections import UserDict
import json
import yaml
import logging
from pathlib import Path
from typing import Union

from fromconfig.core.base import FromConfig
from fromconfig.core.register import register
from fromconfig.utils.libimport import try_import


_jsonnet = try_import("_jsonnet")


LOGGER = logging.getLogger(__name__)


@register("Config")
class Config(FromConfig, UserDict):
    """Help with serialization of dictionaries."""

    @classmethod
    def fromconfig(cls, config):
        return cls(config.get("config", config))


def load(path: Union[str, Path]):
    """Load dictionary from path.

    Parameters
    ----------
    path : Union[str, Path]
        Path to file or yaml / json string
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
        Path to json or yaml file.
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
