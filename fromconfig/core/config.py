"""Base Config Class."""

from collections.abc import MutableMapping
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
    LOGGER.error(f"Unable to import jsonnet, {e}")
    _jsonnet = None


@register("Config")
class Config(FromConfig, MutableMapping):
    """Base Config class (custom dict)."""

    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def __getitem__(self, item):
        return self._kwargs[item]

    def __setitem__(self, key, value):
        self._kwargs[key] = value

    def __delitem__(self, key):
        self._kwargs.__delitem__(key)

    def __iter__(self):
        yield from self._kwargs

    def __len__(self):
        return len(self._kwargs)

    def dump(self, path: Union[str, Path]):
        suffix = Path(path).suffix
        if Path(path).suffix == ".yaml":
            with Path(path).open("w") as file:
                yaml.dump(self._kwargs, file)
        if suffix in (".json", ".jsonnet"):
            with Path(path).open("w") as file:
                json.dump(self._kwargs, file)
        raise ValueError(f"Unable to resolve method for path {path}")

    def dumps(self):
        return yaml.dump(self._kwargs)

    @classmethod
    def fromconfig(cls, config: MutableMapping):
        return cls(**config.get("config", config))

    @classmethod
    def load(cls, path: Union[str, Path]):
        """Load config from path.

        Parameters
        ----------
        path : Union[str, Path]
            Path to file or yaml / json string
        """
        suffix = Path(path).suffix
        if Path(path).suffix == ".yaml":
            with Path(path).open() as file:
                return cls(**yaml.safe_load(file))
        if suffix == ".json":
            with Path(path).open() as file:
                return cls(**json.load(file))
        if Path(path).suffix == ".jsonnet":
            if _jsonnet is None:
                raise ImportError("Unable to import jsonnet.")
            return cls(**json.loads(_jsonnet.evaluate_file(str(path))))
        raise ValueError(f"Unable to resolve method for path {path}")

    @classmethod
    def loads(cls, data: str):
        return cls(**yaml.safe_load(data))
