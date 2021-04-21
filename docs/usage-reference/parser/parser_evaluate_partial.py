"""EvaluateParser partial example."""

import functools

import fromconfig


if __name__ == "__main__":
    config = {"_attr_": "str", "_eval_": "partial", "_args_": ["hello world"]}
    parser = fromconfig.parser.EvaluateParser()
    parsed = parser(config)
    fn = fromconfig.fromconfig(parsed)
    assert isinstance(fn, functools.partial)
    assert fn() == "hello world"
