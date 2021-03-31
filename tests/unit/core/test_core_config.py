"""Tests for core.config."""

import json
import yaml
from pathlib import Path

import pytest

import fromconfig


def test_core_config_no_jsonnet(tmpdir, monkeypatch):
    """Test jsonnet missing handling."""
    monkeypatch.setattr(fromconfig.core.config, "_jsonnet", None)

    # No issue to dump even if missing
    config = {"x": 2}
    fromconfig.dump(config, str(tmpdir.join("config.jsonnet")))
    fromconfig.dump(config, str(tmpdir.join("config.json")))
    fromconfig.dump(config, str(tmpdir.join("config.yaml")))
    fromconfig.dump(config, str(tmpdir.join("config.yml")))

    # No issue to load non-jsonnet files
    assert fromconfig.load(str(tmpdir.join("config.json"))) == config
    assert fromconfig.load(str(tmpdir.join("config.yaml"))) == config
    assert fromconfig.load(str(tmpdir.join("config.yml"))) == config

    # Raise import error if reloading from jsonnet
    with pytest.raises(ImportError):
        fromconfig.load(str(tmpdir.join("config.jsonnet")))


def test_core_config():
    """Test Config."""
    config = fromconfig.Config(x=1)
    assert config["x"] == 1
    assert list(config) == ["x"]
    config["x"] = 2
    assert config["x"] == 2


def test_core_config_is_json_serializable():
    """Test that Config is json serializable."""
    config = fromconfig.Config(x=1)
    assert json.dumps(config) == '{"x": 1}'


@pytest.mark.parametrize(
    "path,serializer",
    [
        pytest.param("config.json", json),
        pytest.param("config.jsonnet", json),
        pytest.param("config.yaml", yaml),
        pytest.param("config.yml", yaml),
        pytest.param("config.xml", None),
    ],
)
def test_core_config_load_dump(path, serializer, tmpdir):
    """Test Config.load."""
    config = {"x": 1}
    path = str(tmpdir.join(path))

    if serializer is None:
        # Incorrect path (not supported)
        with pytest.raises(ValueError):
            fromconfig.dump(config, path)

        with pytest.raises(ValueError):
            fromconfig.load(path)

    else:
        # Dump config to file
        with Path(path).open("w") as file:
            serializer.dump(config, file)

        # Read content of the dump
        with Path(path).open() as file:
            content = file.read()

        # Reload
        reloaded = fromconfig.load(path)
        assert reloaded == config

        # Dump with config method and check content is the same as before
        fromconfig.dump(reloaded, path)
        with Path(path).open() as file:
            assert file.read() == content


@pytest.mark.parametrize(
    "config, expected",
    [
        pytest.param(
            {"_attr_": "str", "_args_": "hello"}, fromconfig.Config(_attr_="str", _args_="hello"), id="simple"
        ),
        pytest.param(
            {"_config_": {"_attr_": "str", "_args_": "hello"}},
            fromconfig.Config(_attr_="str", _args_="hello"),
            id="config",
        ),
    ],
)
def test_core_config_fromconfig(config, expected):
    """Test Config.fromconfig."""
    assert fromconfig.Config.fromconfig(config) == expected
