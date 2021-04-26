"""Config serialization utilities."""

from pathlib import Path
from typing import Union, Any, IO, Dict
import json
import logging
import os
from operator import itemgetter
import re
import io

import yaml

from fromconfig.core import base
from fromconfig.utils import try_import, merge_dict, is_pure_iterable, is_mapping


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
    def fromconfig(cls, config: Any):
        if is_mapping(config):
            return cls(config.get("_config_", config))
        return cls(config)


_YAML_MERGE = "<<:"

_YAML_INCLUDE = "!include"


class IncludeLoader(yaml.SafeLoader):
    """YAML Loader with `!include` constructor to load files."""

    def __init__(self, stream: IO) -> None:
        """Initialize Loader."""
        try:
            self.root = os.path.split(stream.name)[0]
        except AttributeError:
            self.root = os.path.curdir
        super().__init__(stream)


def include(loader, node: yaml.Node) -> Any:
    """Include file referenced at node."""
    path = os.path.join(loader.root, loader.construct_scalar(node))
    return load(path)


IncludeLoader.add_constructor(_YAML_INCLUDE, include)


def yaml_load(stream, Loader):  # pylint: disable=invalid-name
    """Custom yaml load to handle !include and merges."""

    def _expand_includes(s: IO) -> IO:
        """Expand includes before merging.

        The IncludeLoader does not work with the YAML merge key.

        The trick here is to force the include to be loaded into a new
        key, generated from the line number ('{idx}!include<<')

        Parameters
        ----------
        s : io.BaseStream
            A data stream (typically an opened file)

        Returns
        -------
        str
        """
        content = ""
        for idx, line in enumerate(s.readlines()):
            if re.match(f"{_YAML_MERGE} *{_YAML_INCLUDE} *.*", line):
                line = re.sub(f"{_YAML_MERGE} ", line, f"{idx}{_YAML_INCLUDE}{_YAML_MERGE} ")
            content += line
        result = io.StringIO(content)
        setattr(result, "name", stream.name)  # Forward name for Loader
        return result

    def _merge_includes(item: Any) -> Any:
        """Merge includes.

        After expand and YAML parsing, some of the keys are idx<<: which
        were originally intended to be merged to the top level.

        Parameters
        ----------
        item : Any
            Any node of the parsed YAML stream.

        Returns
        -------
        Any
        """
        if is_mapping(item):
            result = {}  # type: Dict[Any, Any]
            for key, value in sorted(item.items(), key=itemgetter(0)):
                if key.endswith(f"{_YAML_INCLUDE}<<"):
                    if not is_mapping(value):
                        raise TypeError(f"Expected Mapping-like object but got {value} ({type(value)}")
                    for subkey, subvalue in value.items():
                        # Since YAML provides no guarantee of ordering
                        # a merge with overrides would be ill-defined
                        result = merge_dict(result, {subkey: _merge_includes(subvalue)}, allow_override=False)
                else:
                    result[key] = _merge_includes(value)
            return result
        if is_pure_iterable(item):
            return [_merge_includes(it) for it in item]
        return item

    return _merge_includes(yaml.load(_expand_includes(stream), Loader))


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
            try:
                return yaml_load(file, IncludeLoader)
            except Exception as e:  # pylint: disable=broad-except
                LOGGER.error(f"Unable to use custom yaml_load ({e}), using yaml.safe_load instead.")
                return yaml.safe_load(file)
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
            json.dump(config, file, indent=4)
    else:
        raise ValueError(f"Suffix {suffix} not recognized for path {path}")
