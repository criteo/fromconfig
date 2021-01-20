"""Simple example.

Example
-------
    fromconfig run config.yaml - trainer - run
"""

import time


class Model:
    """Dummy Model class."""

    def __init__(self, dim: int):
        self.dim = dim

    def __repr__(self):
        return f"{self.__class__.__name__}({self.dim})"


class Trainer:
    """Dummy Trainer class."""

    def __init__(self, model: Model, optimizer: str):
        self.model = model
        self.optimizer = optimizer

    def run(self):
        print(f"Training {self.model} with {self.optimizer}")
        time.sleep(1)
        print("- done.")
