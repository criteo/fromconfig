import mlflow


class Model:
    def __init__(self, learning_rate: float):
        self.learning_rate = learning_rate

    def train(self):
        print(f"Training model with learning_rate {self.learning_rate}")
        if mlflow.active_run() is not None:
            mlflow.log_metric("loss", 0)
