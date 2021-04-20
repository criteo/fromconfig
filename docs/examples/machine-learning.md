### Machine Learning <!-- {docsify-ignore} -->

`fromconfig` is particularly well suited for Machine Learning as it is common to have a lot of different parameters, sometimes far down the call stack, and different configurations of these hyper-parameters.

Given a module `ml.py` defining model, optimizer and trainer classes

```python
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

    def __init__(self, model, optimizer):
        self.model = model
        self.optimizer = optimizer

    def run(self):
        print(f"Training {self.model} with {self.optimizer}")
```

And the following config files

```yaml
# trainer.yaml: configures the training pipeline
trainer:
    _attr_: "training.Trainer"
    model: "@model"
    optimizer: "@optimizer"

# model.yaml: configures the model
model:
    _attr_: "training.Model"
    dim: "@params.dim"

# optimizer.yaml: configures the optimizer
optimizer:
    _attr_: "training.Optimizer"
    learning_rate: @params.learning_rate

# params/small.yaml: hyper-parameters for a small version of the model
params:
    dim: 10
    learning_rate: 0.01

# params/big.yaml: hyper-parameters for a big version of the model
params:
    dim: 100
    learning_rate: 0.001
```

It is possible to launch two different trainings with different set of hyper-parameters with

```bash
fromconfig trainer.yaml model.yaml optimizer.yaml params/small.yaml - trainer - run
fromconfig trainer.yaml model.yaml optimizer.yaml params/big.yaml - trainer - run
```

which should print

```
Training Model(dim=10) with Optimizer(learning_rate=0.01)
Training Model(dim=100) with Optimizer(learning_rate=0.001)
```

This example can be found in [`examples/ml`](examples/ml).

Note that it is encouraged to save these config files with the experiment's files to get full reproducibility. [MlFlow](https://mlflow.org) is an open-source platform that tracks your experiments by logging metrics and artifacts.

