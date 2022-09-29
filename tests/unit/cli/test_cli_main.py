"""Tests for cli.main."""

import fromconfig
from fromconfig.cli.main import parse_args
import sys
from unittest.mock import patch

import subprocess


def capture(command):
    """Utility to execute and capture the result of a command."""
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    return out, err, proc.returncode


def test_cli_parse_args():
    """Test cli.parse_args."""
    argv = ["fromconfig", "config.yaml", "params.yaml", "-", "model", "-", "train"]
    with patch.object(sys, "argv", argv):
        paths, overrides, command = parse_args()
        expected_paths = ["config.yaml", "params.yaml"]
        expected_overrides = {}
        expected_command = "model - train"
        assert paths == expected_paths
        assert overrides == expected_overrides
        assert command == expected_command

    argv = ["fromconfig", "config.yaml", "--output", "/tmp", "-", "run"]
    with patch.object(sys, "argv", argv):
        paths, overrides, command = parse_args()
        expected_paths = ["config.yaml"]
        expected_overrides = {"output": "/tmp"}
        expected_command = "run"
        assert paths == expected_paths
        assert overrides == expected_overrides
        assert command == expected_command

    argv = ["fromconfig", "config.yaml", "--output=/tmp", "-", "run"]
    with patch.object(sys, "argv", argv):
        paths, overrides, command = parse_args()
        expected_paths = ["config.yaml"]
        expected_overrides = {"output": "/tmp"}
        expected_command = "run"
        assert paths == expected_paths
        assert overrides == expected_overrides
        assert command == expected_command


def test_cli_main_nothing():
    """Test that fromconfig with no argument does not error."""
    out, err, exitcode = capture(["fromconfig"])
    assert exitcode == 0, (out, err)
    assert all(word in out for word in [b"fromconfig", b"flags"])
    assert err == b""


def test_cli_main(tmpdir):
    """Test cli.main."""
    # Write parameters
    path_parameters = tmpdir.join("parameters.yaml")
    parameters = {"value": "hello world"}

    fromconfig.dump(parameters, path_parameters)

    # Write config
    path_config = tmpdir.join("config.yaml")
    config = {"run": {"_attr_": "print", "_args_": ["${value}"]}}
    fromconfig.dump(config, path_config)

    # Execute command and check result
    command = ["fromconfig", path_config, path_parameters, "-", "run"]
    out, err, exitcode = capture(command)
    assert exitcode == 0, (out, err)
    assert out == b"hello world\n"
    assert err == b""
