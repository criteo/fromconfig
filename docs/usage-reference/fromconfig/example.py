"""Simple example."""

import fromconfig


if __name__ == "__main__":
    config = {"_attr_": "str", "_args_": [1]}
    assert fromconfig.fromconfig(config) == '1'
