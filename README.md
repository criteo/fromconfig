# FromConfig

Create object from config files. Makes it easy to launch jobs from config files with a generic command line.

## Features

* short command line with config file instead of long command line (eg with fire), much more readable, possible to commit the config, ...
* avoid passing arguments down the call stack, and instead configure classes directly
* compose configs in different files

## Install

```bash
pip install fromconfig
```

## Usage

### With a parser

Run `fromconfig run config.yaml - trainer - run`

```yaml
model:
  _attr_: "model.Model"
  dim: 100

trainer:
  _attr_: "model.Trainer"
  model: "@model"
  optimizer: "SGD"
```

```python
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
```


### Manually

```python
from fromconfig import fromconfig


class Model:
    """Custom Model defined in current module."""

    def __init__(self, dim: int, learning_rate: float):
        self.dim = dim
        self.learning_rate = learning_rate


config = {
    "_attr_": "__main__.Model",
    "dim": 100,
    "learning_rate": 0.1
}
model = fromconfig(config)
```

## Architecture

Split in 2 parts
* core that takes dict and build instances
* parser that makes it easier to add syntactic sugar
* support for custom from_config implementation : possible to inherit from_config

## Related

Similar systems exist:
* [fire](https://github.com/google/python-fire) command line from python functions
* [omegaconf](https://github.com/omry/omegaconf) configuration system for python using yaml
* [hydra](https://hydra.cc/docs/intro/) higher level layer on top of omegaconf (compose several files, defaults, ...)
* [gin](https://github.com/google/gin-config) dependency injection for configuration in python
* [thinc](https://thinc.ai/) define arbitrary trees of objects in config files for python
