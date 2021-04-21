"""SingletonParser example."""

import fromconfig


if __name__ == "__main__":
    config = {
        "x": {"_attr_": "dict", "_singleton_": "my_dict", "x": 1},
        "y": {"_attr_": "dict", "_singleton_": "my_dict", "x": 1},
    }
    parser = fromconfig.parser.SingletonParser()
    parsed = parser(config)
    instance = fromconfig.fromconfig(parsed)
    assert id(instance["x"]) == id(instance["y"])
