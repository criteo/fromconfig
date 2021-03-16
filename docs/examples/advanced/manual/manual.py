"""Manual Example."""

from dataclasses import dataclass

import fromconfig


@dataclass
class Model:
    """Dummy Model class."""

    dim: int


@dataclass
class Optimizer:
    """Dummy Optimizer class."""

    learning_rate: float


class Trainer:
    """Dummy Trainer class."""

    def __init__(self, model, optimizer):
        self.model = model
        self.optimizer = optimizer

    def run(self):
        print(f"Training {self.model} with {self.optimizer}")


if __name__ == "__main__":
    config = {
        "trainer": {"_attr_": "Trainer", "model": "@model", "optimizer": "@optimizer"},
        "model": {"_attr_": "Model", "dim": 10},
        "optimizer": {"_attr_": "Optimizer", "learning_rate": 0.001},
    }

    # Parse config (replace references as "@model")
    parser = fromconfig.parser.DefaultParser()
    parsed = parser(config)

    # Instantiate trainer and call run()
    trainer = fromconfig.fromconfig(parsed["trainer"])
    trainer.run()
