"""Machine Learning Example code."""

from dataclasses import dataclass


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

    def __init__(self, model, optimizer, path):
        self.model = model
        self.optimizer = optimizer
        self.path = path

    def run(self):
        print(f"Training {self.model} with {self.optimizer}")
        print(f"Saving {self.model} to {self.path}")
