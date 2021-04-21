"""EvaluateParser call example."""

import fromconfig


if __name__ == "__main__":
    config = {"_attr_": "str", "_eval_": "call", "_args_": ["hello world"]}
    parser = fromconfig.parser.EvaluateParser()
    parsed = parser(config)
    assert fromconfig.fromconfig(parsed) == "hello world"
