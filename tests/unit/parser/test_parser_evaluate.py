"""Tests for parser.evaluate."""

import pytest

import fromconfig


@pytest.mark.parametrize(
    "config, expected",
    [
        pytest.param({"_attr_": "str", "_eval_": "import"}, str, id="import"),
        pytest.param({"_attr_": "str", "_args_": ["hello"], "_eval_": "call"}, "hello", id="call"),
        pytest.param({"_attr_": "str", "_args_": ["hello"], "_eval_": "partial"}, lambda: "hello", id="partial"),
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
