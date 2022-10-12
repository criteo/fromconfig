"""Tests for parser.evaluate."""

import pytest
from unittest import mock

import fromconfig


@pytest.mark.parametrize(
    "config, expected",
    [
        pytest.param(None, None, id="none"),
        pytest.param({"a": 1, "b": 2}, {"a": 1, "b": 2}, id="dummy_mapping"),
        pytest.param({"_attr_": "str", "_eval_": "import"}, str, id="import"),
        pytest.param({"_attr_": "str", "_args_": ["hello"], "_eval_": "call"}, "hello", id="call"),
        pytest.param({"_attr_": "str", "_args_": ["hello"], "_eval_": "partial"}, lambda: "hello", id="partial"),
        pytest.param(
            {"_attr_": "str", "_args_": [{"hello": "world"}], "_eval_": "partial"},
            lambda: "{'hello': 'world'}",
            id="partial_with_dummy_mapping",
        ),
    ],
)
def test_parser_evaluate(config, expected):
    """Test parser.EvaluateParser."""
    parser = fromconfig.parser.EvaluateParser()
    parsed = parser(config)
    if callable(expected):
        assert fromconfig.fromconfig(parsed)() == expected()
    else:
        assert fromconfig.fromconfig(parsed) == expected


def fake_data_loader(path, number_of_line, is_server_up=False, use_custom_header=False):
    return (
        f"Loaded {number_of_line} lines of data from {path}. Server was up: {is_server_up}, "
        f"custom header was used: {use_custom_header}"
    )


def find_latest_path():
    """This function returns the path of the data to be loaded.
    This path could be unknown at the launch of the pipeline.
    """
    return "latest/path/to/data"


def ping_server(server_address):
    """This function pings the server to determine if it is up.
    It will be called when the data loader will be launched.
    """
    return server_address == "localhost"


@mock.patch(__name__ + ".find_latest_path", return_value=find_latest_path())
@mock.patch(__name__ + ".ping_server", return_value=ping_server("localhost"))
def test_parser_evaluate_lazy(find_latest_path_mock, ping_server_mock):
    """Test that lazy arguments are evaluated after the function is called."""

    config = {
        "_attr_": "fake_data_loader",
        "_args_": [{"_attr_": "find_latest_path", "_eval_": "lazy"}, 1000],
        "is_server_up": {"_attr_": "ping_server", "server_address": "localhost", "_eval_": "lazy"},
        "use_custom_header": False,
        "_eval_": "partial",
    }
    parser = fromconfig.parser.EvaluateParser()
    parsed = parser(config)
    data_loader_job = fromconfig.fromconfig(parsed)
    # The lazy constructors should not have been called before the job has been launched
    find_latest_path_mock.assert_not_called()
    ping_server_mock.assert_not_called()

    expected_answer = (
        "Loaded 1000 lines of data from latest/path/to/data. Server was up: True, custom header was used: False"
    )
    assert data_loader_job() == expected_answer
    find_latest_path_mock.assert_called_once()
    ping_server_mock.assert_called_once()


def fake_heavy_computations():
    """This function performs heavy computations, therefore we want to evaluate it only once."""
    return 2


def multiply(a, b):
    return a * b


@mock.patch(__name__ + ".fake_heavy_computations", return_value=fake_heavy_computations())
def test_parser_evaluate_lazy_with_memoization(heavy_computations_mock):
    """Test that lazy arguments with memoization are only evaluated once."""
    config = {
        "_attr_": "multiply",
        "_eval_": "partial",
        "a": {"_attr_": "fake_heavy_computations", "_eval_": "lazy", "_memoization_key_": "fake_heavy_computations"},
        "b": {"_attr_": "fake_heavy_computations", "_eval_": "lazy", "_memoization_key_": "fake_heavy_computations"},
    }
    parser = fromconfig.parser.EvaluateParser()
    parsed = parser(config)
    multiply_partial = fromconfig.fromconfig(parsed)
    heavy_computations_mock.assert_not_called()
    assert multiply_partial() == 4
    heavy_computations_mock.assert_called_once()


@pytest.mark.parametrize(
    "config, exception",
    [
        pytest.param({"_attr_": "str", "_args_": ["hello"], "_eval_": "import"}, ValueError, id="import+args"),
        pytest.param({"_attr_": "dict", "x": 1, "_eval_": "import"}, ValueError, id="import+kwargs"),
        pytest.param({"x": 1, "_eval_": "import"}, KeyError, id="import+noattr"),
        pytest.param({"x": 1, "_eval_": "partial"}, KeyError, id="partial+noattr"),
    ],
)
def test_parser_evaluate_exceptions(config, exception):
    """Test parser.EvaluateParser exceptions."""
    parser = fromconfig.parser.EvaluateParser()
    with pytest.raises(exception):
        parser(config)
