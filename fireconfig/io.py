"""Read utilities."""

from typing import Union, Dict
import logging
import json
import yaml
from pathlib import Path

try:
    import _jsonnet
except ImportError as e:
    print(f"Unable to import jsonnet, {e}")


LOGGER = logging.getLogger(__name__)


def read(path: Union[str, Path]) -> Dict:
    """Read json string or json, jsonnet or yaml files."""
    if Path(path).suffix == ".json":
        return read_json(path)
    if Path(path).suffix == ".jsonnet":
        return read_jsonnet(path)
    if Path(path).suffix == ".yaml":
        return read_yaml(path)
    if is_json(path):
        return json.loads(path)
    raise ValueError(f"Unable to read {path} (must be json string or json/jsonnet/yaml file.")


def read_json(path: Union[str, Path]) -> Dict:
    """Read json file into dictionary."""
    with Path(path).open() as file:
        return json.load(file)


def read_jsonnet(path: Union[str, Path]) -> Dict:
    """Read jsonnet file into dictionary."""
    json_str = _jsonnet.evaluate_file(str(path))
    return json.loads(json_str)


def read_yaml(path: Union[str, Path]) -> Dict:
    with Path(path).open() as file:
        return yaml.load(file)


def is_json(data: str) -> bool:
    """Return True if data is a valid json string else False"""
    try:
        json.loads(data)
    except ValueError:
        return False
    return True
