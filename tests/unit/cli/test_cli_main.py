"""Tests for cli.main."""

import fromconfig

import subprocess


def capture(command):
    """Utility to execute and capture the result of a commmand."""
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    return out, err, proc.returncode


def test_cli_main(tmpdir):
    """Test cli.main."""
    # Write parameters
    path_parameters = tmpdir.join("parameters.yaml")
    parameters = {"value": "hello world"}

    fromconfig.dump(parameters, path_parameters)

    # Write config
    path_config = tmpdir.join("config.yaml")
    config = {"run": {"_attr_": "print", "_args_": ["@value"]}}
    fromconfig.dump(config, path_config)

    # Execute command and check result
    command = ["fromconfig", path_config, path_parameters, "-", "run"]
    out, err, exitcode = capture(command)
    assert exitcode == 0, (out, err)
    assert out == b"hello world\n"
    assert err == b""
