"""Config Class."""

from collections import UserDict
import json
import yaml
import logging
from pathlib import Path
from typing import Union

from fromconfig.core.base import FromConfig
from fromconfig.core.register import register


LOGGER = logging.getLogger(__name__)

try:
    import _jsonnet
except ImportError as e:
    LOGGER.error(f"Unable to import _jsonnet, {e}")
    _jsonnet = None


@register("Config")
class Config(FromConfig, UserDict):
    """Help with serialization of dictionaries."""

    def dump(self, path: Union[str, Path]):
        """Dump dictionary content to file in path.

        Parameters
        ----------
        path : Union[str, Path]
            Path to json or yaml file.
        """
        suffix = Path(path).suffix
        if suffix in (".yaml", ".yml"):
            with Path(path).open("w") as file:
                yaml.dump(self.data, file)
        if suffix in (".json", ".jsonnet"):
            with Path(path).open("w") as file:
                json.dump(self.data, file)
        raise ValueError(f"Unable to resolve method for path {path}")

    @classmethod
    def load(cls, path: Union[str, Path]):
        """Load dictionary from path.

        Parameters
        ----------
        path : Union[str, Path]
            Path to file or yaml / json string
        """
        suffix = Path(path).suffix
        if suffix in (".yaml", ".yml"):
            with Path(path).open() as file:
                return cls(yaml.safe_load(file))
        if suffix == ".json":
            with Path(path).open() as file:
                return cls(json.load(file))
        if suffix == ".jsonnet":
            if _jsonnet is None:
                raise ImportError("Unable to import _jsonnet.")
            return cls(json.loads(_jsonnet.evaluate_file(str(path))))
        raise ValueError(f"Unable to resolve method for path {path}")

    @classmethod
    def fromconfig(cls, config):
        return cls(config.get("config", config))
