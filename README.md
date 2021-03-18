# FromConfig
[![pypi](https://img.shields.io/pypi/v/fromconfig.svg)](https://pypi.python.org/pypi/fromconfig)
[![ci](https://github.com/criteo/fromconfig/workflows/Continuous%20integration/badge.svg)](https://github.com/criteo/fromconfig/actions?query=workflow%3A%22Continuous+integration%22)

A library to instantiate any Python object from configuration files.

Thanks to [Python Fire](https://github.com/google/python-fire), `fromconfig` acts as a generic command line interface from configuration files *with absolutely no change to the code*.


![FromConfig](https://raw.githubusercontent.com/criteo/fromconfig/master/docs/images/fromconfig.svg)

## Table Of Content

<!-- MarkdownTOC -->

- [Install](#install)
- [Quickstart](#quickstart)
- [Cheat Sheet](#cheat-sheet)
- [Why FromConfig ?](#why-fromconfig-)
- [Usage Reference](#usage-reference)
    - [Command Line](#command-line)
    - [Config syntax](#config-syntax)
    - [Parsing](#parsing)
        - [Default](#default)
        - [OmegaConf](#omegaconf)
        - [References](#references)
        - [Evaluate](#evaluate)
        - [Singleton](#singleton)
- [Examples](#examples)
    - [Manual](#manual)
    - [Custom Parser](#custom-parser)
    - [Custom FromConfig](#custom-fromconfig)
    - [Machine Learning](#machine-learning)
    - [Hyper-Parameter Search](#hyper-parameter-search)
- [Development](#development)

<!-- /MarkdownTOC -->


<a id="install"></a>
## Install

```bash
pip install fromconfig
```

<a id="quickstart"></a>
## Quickstart

`fromconfig` can configure any Python object, without any change to the code.

As an example, let's consider a `foo.py` module

```python
class Model:
    def __init__(self, learning_rate: float):
        self.learning_rate = learning_rate

    def train(self):
        print(f"Training model with learning_rate {self.learning_rate}")
```

with the following config files
- `config.yaml`
```yaml
model:
  _attr_: foo.Model
  learning_rate: "@params.learning_rate"
```
- `params.yaml`
```yaml
params:
  learning_rate: 0.1
```

In a terminal, run

```bash
fromconfig config.yaml params.yaml - model - train
```

which prints
```
Training model with learning_rate 0.1
```

Here is a step-by-step breakdown of what is happening

1. Load the yaml files into dictionaries
2. Merge the dictionaries
3. After parsing the resulting dictionary with a default parser (resolving references as `@params.learning_rate`, etc.), it recursively instantiate sub-dictionaries, using the `_attr_` key to resolve the Python class / function as an import string.
4. Finally, the `- model - train` part of the command is a [Python Fire](https://github.com/google/python-fire) syntax, which translates into "get the `model` key from the instantiated dictionary and execute the `train` method".

This example can be found in [`docs/examples/quickstart`](docs/examples/quickstart).

To learn more about `FromConfig` features, see the [Usage Reference](#usage-reference) and [Examples](#examples) sections.


<a id="cheat-sheet"></a>
## Cheat Sheet

`fromconfig.fromconfig` special keys


| Key        | Value Example     | Use                                               |
|------------|-------------------|---------------------------------------------------|
| "\_attr\_" | "foo.bar.MyClass" | Full import string of a class, function or method |
| "\_args\_" | [1, 2]            | Positional arguments                              |

`fromconfig.parser.DefaultParser` syntax

| Key             | Value                         | Use                                    |
|-----------------|-------------------------------|----------------------------------------|
| "\_singleton\_" | "my_singleton_name"           | Creates a singleton identified by name |
| "\_eval\_"      | "call", "import", "partial"   | Evaluation modes                       |
|                 | "@params.model"               | Reference                              |
|                 | "${params.url}:${params.port} | Interpolation via OmegaConf            |

<a id="why-fromconfig-"></a>
## Why FromConfig ?

`fromconfig` enables the instantiation of arbitrary trees of Python objects from config files.

It echoes the `FromParams` base class of [AllenNLP](https://github.com/allenai/allennlp).

It is particularly well suited for __Machine Learning__ (see [examples](#machine-learning)). Launching training jobs on remote clusters requires custom command lines, with arguments that need to be propagated through the call stack (e.g., setting parameters of a particular layer). The usual way is to write a custom command with a reduced set of arguments, combined by an assembler that creates the different objects. With `fromconfig`, the command line becomes generic, and all the specifics are kept in config files. As a result, this preserves the code from any backwards dependency issues and allows full reproducibility by saving config files as jobs' artifacts. It also makes it easier to merge different sets of arguments in a dynamic way through references and interpolation.


`fromconfig` is based off the config system developed as part of the [deepr](https://github.com/criteo/deepr) library, a collections of utilities to define and train Tensorflow models in a Hadoop environment.

Other relevant libraries are:
* [fire](https://github.com/google/python-fire) automatically generate command line interface (CLIs) from absolutely any Python object.
* [omegaconf](https://github.com/omry/omegaconf) YAML based hierarchical configuration system with support for merging configurations from multiple sources.
* [hydra](https://hydra.cc/docs/intro/) A higher-level framework based off `omegaconf` to configure complex applications.
* [gin](https://github.com/google/gin-config) A lightweight configuration framework based on dependency injection.
* [thinc](https://thinc.ai/) A lightweight functional deep learning library that comes with an integrated config system


<a id="usage-reference"></a>
## Usage Reference

The `fromconfig` library relies on two independent components.

1. A lightweight __syntax__ to instantiate any Python object from dictionaries (using special keys `_attr_` and `_args_`).
2. A composable, flexible, and customizable framework to __parse__ configs before instantiation. This allows configs to remain short and readable with syntactic sugar to define singletons, references, etc.

<a id="command-line"></a>
### Command Line

Usage : call `fromconfig` on any number of paths to config files.

```bash
fromconfig config.yaml params.yaml
```

Supported formats : YAML, JSON, and [JSONNET](https://jsonnet.org).

The command line loads the different config files into Python dictionaries and merge them (it fails in case of any key conflict). It parses the resulting dictionary with the `DefaultParser` before calling `fromconfig.fromconfig` to instantiate the object.

As the `fromconfig` command is wrapped in a [Python Fire](https://github.com/google/python-fire) call, you can manipulate the resulting instantiated dictionary via the command line by using the fire syntax.

For example `fromconfig config.yaml - name` instantiates the dictionary defined in `config.yaml` and gets the value associated with the key `name`.

<a id="config-syntax"></a>
### Config syntax

The `fromconfig.fromconfig` function recursively instantiates objects from dictionaries.

It uses two special keys
- `_attr_`: (optional) full import string to any Python object.
- `_args_`: (optional) positional arguments.

For example

```python
import fromconfig

config = {"_attr_": "str", "_args_": [1]}

fromconfig.fromconfig(config)  # '1'
```

`FromConfig` resolves the builtin type `str` from the `_attr_` key, and creates a new string with the positional arguments defined in `_args_`, in other words `str(1)` which return `'1'`.

If the `_attr_` key is not given, then the dictionary is left as a dictionary (the values of the dictionary may be recursively instantiated).

If other keys are available in the dictionary, they are treated as key-value arguments (`kwargs`).

For example

```python
import fromconfig


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


config = {
    "_attr_": "Point",
    "x": 0,
    "y": 0
}
fromconfig.fromconfig(config)  # Point(0, 0)
```

Note that during instantiation, the config object is not modified. Also, any mapping-like container is supported (there is no special "config" class in `fromconfig`).

<a id="parsing"></a>
### Parsing

<a id="default"></a>
#### Default

`FromConfig` comes with a default parser which sequentially applies
- `OmegaConfParser`: can be practical for interpolation
- `ReferenceParser`: resolves references
- `EvaluateParser`: syntactic sugar to configure `functool.partial` or simple imports
- `SingletonParser`: syntactic sugar to define singletons

For example, let's see how to create singletons, use references and interpolation

```python
import fromconfig


class Model:
    def __init__(self, model_dir):
        self.model_dir = model_dir


class Trainer:
    def __init__(self, model):
        self.model = model


config = {
    "model": {
        "_attr_": "Model",
        "_singleton_": "my_model",  # singleton
        "model_dir": "${data.root}/${data.model}"  # interpolation
    },
    "data": {
        "root": "/path/to/root",
        "model": "subdir/for/model"
    },
    "trainer": {
        "_attr_": "Trainer",
        "model": "@model",  # reference
    }
}
parser = fromconfig.parser.DefaultParser()
parsed = parser(config)
instance = fromconfig.fromconfig(parsed)
id(instance["model"]) == id(instance["trainer"].model)  # True
instance["model"].model_dir == "/path/to/root/subdir/for/model"  # True
```

<a id="omegaconf"></a>
#### OmegaConf

[OmegaConf](https://omegaconf.readthedocs.io) is a YAML based hierarchical configuration system with support for merging configurations from multiple sources. The `OmegaConfParser` wraps some of its functionality (for example, variable interpolation).

For example

```python
import fromconfig
config = {
    "host": "localhost",
    "port": "8008",
    "url": "${host}:${port}"
}
parser = fromconfig.parser.OmegaConfParser()
parsed = parser(config)
parsed["url"]  # 'localhost:8008'
````

Learn more on the [OmegaConf documentation website](https://omegaconf.readthedocs.io).

<a id="references"></a>
#### References

To make it easy to compose different configuration files and avoid deeply nested config dictionaries, you can use the `ReferenceParser`.

For example,

```python
import fromconfig
parser = fromconfig.parser.ReferenceParser()
config = {"params": {"x": 1}, "y": "@params.x"}
parsed = parser(config)
parsed["y"]
```

The `ReferenceParser` looks for values starting with a `@`, then split by `.`, and navigate from the top-level dictionary.

In practice, it makes configuration files more readable (flat) and avoids duplicates.

It is also a convenient way to dynamically compose different configs.

For example

```python
import fromconfig

param1 = {
    "params": {
        "x": 1
    }
}
param2 = {
    "params": {
        "x": 2
    }
}
config = {
    "model": {
        "x": "@params.x"
    }
}
parser = fromconfig.parser.ReferenceParser()
parsed1 = parser({**config, **param1})
parsed1["model"]["x"]  # 1
parsed2 = parser({**config, **param2})
parsed1["model"]["x"]  # 2
```

<a id="evaluate"></a>
#### Evaluate

The `EvaluateParser` makes it possible to simply import a class / function, or configure a constructor via a `functools.partial` call.

The parser uses a special key `_eval_` with possible values
- `call`: standard behavior, results in `attr(kwargs)`.
- `partial`: delays the call, results in a `functools.partial(attr, **kwargs)`
- `import`: simply import the attribute, results in `attr`

__call__

```python
import fromconfig

config = {"_attr_": "str", "_eval_": "call", "_args_": ["hello world"]}
parser = fromconfig.parser.EvaluateParser()
parsed = parser(config)
fromconfig.fromconfig(parsed) == "hello world"  # True
```

__partial__

```python
import fromconfig

config = {"_attr_": "str", "_eval_": "partial", "_args_": ["hello world"]}
parser = fromconfig.parser.EvaluateParser()
parsed = parser(config)
fn = fromconfig.fromconfig(parsed)
isinstance(fn, functools.partial)  # True
fn() == "hello world"  # True
```

__import__

```python
import fromconfig

config = {"_attr_": "str", "_eval_": "import"}
parser = fromconfig.parser.EvaluateParser()
parsed = parser(config)
fromconfig.fromconfig(parsed) is str  # True
```


<a id="singleton"></a>
#### Singleton

To define singletons (typically an object used in multiple places), use the `SingletonParser`.

For example,

```python
import fromconfig


config = {
    "x": {
        "_attr_": "dict",
        "_singleton_": "my_dict",
        "x": 1
    },
    "y": {
        "_attr_": "dict",
        "_singleton_": "my_dict",
        "x": 1
    }
}
parser = fromconfig.parser.SingletonParser()
parsed = parser(config)
instance = fromconfig.fromconfig(parsed)
id(instance["x"]) == id(instance["y"])
```

Without the `_singleton_` entry, two different dictionaries would have been created.

Note that using references is not a solution to create singletons, as the reference mechanism only copies missing parts of the configs.

The parser uses the special key `_singleton_` whose value is the name associated with the instance to resolve singletons at instantiation time.

<a id="examples"></a>
## Examples

<a id="manual"></a>
### Manual

It is possible to manipulate configs directly in the code without using the `fromconfig` CLI.

For example,

```python
"""Manual Example."""

import fromconfig


class Model:
    def __init__(self, learning_rate: float):
        self.learning_rate = learning_rate

    def train(self):
        print(f"Training model with learning_rate {self.learning_rate}")


if __name__ == "__main__":
    # Create config dictionary
    config = {
        "model": {"_attr_": "Model", "learning_rate": "@params.learning_rate"},
        "params": {
            "learning_rate": 0.1
        }
    }

    # Parse config (replace "@params.learning_rate" by its value)
    parser = fromconfig.parser.DefaultParser()
    parsed = parser(config)

    # Instantiate model and call train()
    model = fromconfig.fromconfig(parsed["model"])
    model.train()
```

This example can be found in [`docs/examples/manual`](docs/examples/manual)

<a id="custom-parser"></a>
### Custom Parser

One of `fromconfig`'s strength is its flexibility when it comes to the config syntax.

To reduce the config boilerplate, it is possible to add a new `Parser` to support a new syntax.

Let's cover a dummy example : let's say we want to replace all empty strings with "lorem ipsum".

```python
from typing import Dict

import fromconfig


class LoremIpsumParser(fromconfig.parser.Parser):
    """Custom Parser that replaces empty string by a default string."""

    def __init__(self, default: str = "lorem ipsum"):
        self.default = default

    def __call__(self, config: Dict):

        def _map_fn(value):
            if isinstance(value, str) and not value:
                return self.default
            return value

        # Utility to apply a function to all nodes of a nested dict
        # in a depth-first search
        return fromconfig.utils.depth_map(_map_fn, config)


cfg = {
    "x": "Hello World",
    "y": ""
}
parser = LoremIpsumParser()
parsed = parser(cfg)
print(parsed)  # {"x": "Hello World", "y": "lorem ipsum"}
```

This example can be found in [`docs/examples/custom_parser`](docs/examples/custom_parser)


<a id="custom-fromconfig"></a>
### Custom FromConfig

The logic to instantiate objects from config dictionaries is always the same.

It resolves the class, function or method `attr` from the `_attr_` key, recursively call `fromconfig` on all the other key-values to get a `kwargs` dictionary of objects, and call `attr(**kwargs)`.

It is possible to customize the behavior of `fromconfig` by inheriting the `FromConfig` class.

For example


```python
import fromconfig


class MyClass(fromconfig.FromConfig):

    def __init__(self, x):
        self.x = x

    @classmethod
    def fromconfig(cls, config):
        if "x" not in config:
            return cls(0)
        else:
            return cls(**config)


config = {}
got = MyClass.fromconfig(config)
isinstance(got, MyClass)  # True
got.x  # 0
```

One custom `FromConfig` class is provided in `fromconfig` which makes it possible to stop the instantiation and keep config dictionaries as config dictionaries.

For example

```python
import fromconfig


config = {
    "_attr_": "fromconfig.Config",
    "_config_": {
        "_attr_": "list"
    }
}
fromconfig.fromconfig(config)  # {'_attr_': 'list'}
```

<a id="machine-learning"></a>
### Machine Learning

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

- `trainer.yaml`: configures the training pipeline
```yaml
trainer:
    _attr_: "training.Trainer"
    model: "@model"
    optimizer: "@optimizer"
```
- `model.yaml`: configures the model
```yaml
model:
    _attr_: "training.Model"
    dim: "@params.dim"
```
- `optimizer.yaml`: configures the optimizer
```yaml
optimizer:
    _attr_: "training.Optimizer"
    learning_rate: @params.learning_rate
```
- `params/small.yaml`: hyper-parameters for a small version of the model
```yaml
params:
    dim: 10
    learning_rate: 0.01
```
- `params/big.yaml`: hyper-parameters for a big version of the model
```yaml
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

This example can be found in [`docs/examples/ml`](docs/examples/ml).

Note that it is encouraged to save these config files with the experiment's files to get full reproducibility. [MlFlow](https://mlflow.org) is an open-source platform that tracks your experiments by logging metrics and artifacts.


<a id="hyper-parameter-search"></a>
### Hyper-Parameter Search

To launch an hyper-parameter search, generate config files on the fly if using the `fromconfig` CLI, or config dictionaries.

For example,

```python
import fromconfig


if __name__ == "__main__":
    config = {
        "model": {
            "_attr_": "ml.Model",
            "dim": "@params.dim"
        },
        "optimizer": {
            "_attr_": "ml.Optimizer",
            "learning_rate": "@params.learning_rate"
        },
        "trainer": {
            "_attr_": "ml.Trainer",
            "model": "@model",
            "optimizer": "@optimizer"
        }
    }
    parser = fromconfig.parser.DefaultParser()
    for dim in [10, 100]:
        for learning_rate in [0.01, 0.1]:
            params = {
                "dim": dim,
                "learning_rate": learning_rate
            }
            parsed = parser({**config, "params": params})
            trainer = fromconfig.fromconfig(parsed)["trainer"]
            trainer.run()
```

which prints

```
Training Model(dim=10) with Optimizer(learning_rate=0.01)
Training Model(dim=10) with Optimizer(learning_rate=0.1)
Training Model(dim=100) with Optimizer(learning_rate=0.01)
Training Model(dim=100) with Optimizer(learning_rate=0.1)
```

This example can be found in [`docs/examples/ml`](docs/examples/ml) (run `python hp.py`).


<a id="development"></a>
## Development

To install the library from source in editable mode

```bash
git clone https://github.com/criteo/fromconfig
cd fromconfig
make install
```

To install development tools

```bash
make install-dev
```

To lint the code (mypy, pylint and black)

```bash
make lint
```

To format the code with black

```bash
make black
```
