"""Config example."""

import fromconfig


if __name__ == "__main__":
    config = {"_attr_": "fromconfig.Config", "_config_": {"_attr_": "list"}}
    print(fromconfig.fromconfig(config))  # {'_attr_': 'list'}
