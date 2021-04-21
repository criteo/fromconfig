"""DefaultParser example."""

import fromconfig


class Model:
    def __init__(self, model_dir):
        self.model_dir = model_dir


class Trainer:
    def __init__(self, model):
        self.model = model


if __name__ == "__main__":
    config = {
        "model": {
            "_attr_": "Model",
            "_singleton_": "my_model",  # singleton
            "model_dir": "${data.root}/${data.model}",  # interpolation
        },
        "data": {"root": "/path/to/root", "model": "subdir/for/model"},
        "trainer": {"_attr_": "Trainer", "model": "@model"},  # reference
    }

    # Parse and instantiate
    parser = fromconfig.parser.DefaultParser()
    parsed = parser(config)
    instance = fromconfig.fromconfig(parsed)

    # Check result
    assert id(instance["model"]) == id(instance["trainer"].model)
    assert instance["model"].model_dir == "/path/to/root/subdir/for/model"
