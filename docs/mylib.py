"""Example."""

import fire


class Model:
    """Dummy Model Class."""

    def __init__(self, learning_rate: float):
        self.learning_rate = learning_rate

    def forward(self, batch):
        print(f"Forward pass, batch = {batch}")

    def backward(self, batch):
        print(f"Backward pass, batch = {batch}, learning_rate = {self.learning_rate}")


def get_dataset(path: str):
    """Create Dataset from path."""
    # pylint: disable=unused-argument
    return [{"batch": 0}]


def train_model(model, dataset):
    """Train model on dataset."""
    for batch in dataset:
        model.forward(batch)
        model.backward(batch)


def main(path_dataset: str, learning_rate: float):
    """Reload dataset, create model and train."""
    model = Model(learning_rate)
    dataset = get_dataset(path_dataset)
    train_model(model, dataset)


if __name__ == "__main__":
    fire.Fire(main)
