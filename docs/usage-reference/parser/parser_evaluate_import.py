"""EvaluateParser import example."""

import fromconfig


if __name__ == "__main__":
    config = {"_attr_": "str", "_eval_": "import"}
    parser = fromconfig.parser.EvaluateParser()
    parsed = parser(config)
    assert fromconfig.fromconfig(parsed) is str
