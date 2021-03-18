"""Manual Example."""

import fromconfig


class Model:
    def __init__(self, learning_rate: float):
        self.learning_rate = learning_rate

    def train(self):
        print(f"Training model with learning_rate {self.learning_rate}")


if __name__ == "__main__":
    # Create config dictionary
    config = {"model": {"_attr_": "Model", "learning_rate": "@params.learning_rate"}, "params": {"learning_rate": 0.1}}

    # Parse config (replace references as "@model")
    parser = fromconfig.parser.DefaultParser()
    parsed = parser(config)

    # Instantiate trainer and call run()
    model = fromconfig.fromconfig(parsed["model"])
    model.train()
