"""Dummy Model."""

import mlflow


class Model:
    def __init__(self, learning_rate: float):
        self.learning_rate = learning_rate

    def train(self):
        print(f"Training model with learning_rate {self.learning_rate}")
        if mlflow.active_run():
            mlflow.log_metric("learning_rate", self.learning_rate)
