"""Dummy Model."""


class Model:
    def __init__(self, dim: int, learning_rate: float):
        self.dim = dim
        self.learning_rate = learning_rate

    def train(self):
        print(f"Training model({self.dim}) with learning_rate {self.learning_rate}")
