# FromConfig
[![pypi](https://img.shields.io/pypi/v/fromconfig.svg)](https://pypi.python.org/pypi/fromconfig)
[![ci](https://github.com/criteo/fromconfig/workflows/Continuous%20integration/badge.svg)](https://github.com/criteo/fromconfig/actions?query=workflow%3A%22Continuous+integration%22)

A library to instantiate any Python object from configuration files.

Thanks to [Python Fire](https://github.com/google/python-fire), `fromconfig` acts as a generic command line interface from configuration files *with absolutely no change to the code*.

What are `fromconfig` strengths?

1. __No code change__ Install with `pip install fromconfig` and [get started](#quickstart).
2. __Simplicity__ See the simple [config syntax](#config-syntax) and [command line](#command-line).
3. __Extendability__ See how to write [a custom `Parser`](#custom-parser), [a custom `Launcher`](#custom-launcher), and [a custom `FromConfig` class](#custom-fromconfig).


![FromConfig](https://raw.githubusercontent.com/criteo/fromconfig/master/docs/images/fromconfig.svg)

## Table Of Content

<!-- MarkdownTOC -->

- [Install](#install)
- [Quickstart](#quickstart)
- [Cheat Sheet](#cheat-sheet)
- [Why FromConfig ?](#why-fromconfig-)
- [Usage Reference](#usage-reference)
    - [Command Line](#command-line)
    - [Overrides](#overrides)
    - [Config syntax](#config-syntax)
    - [Parsing](#parsing)
        - [Default](#default)
        - [OmegaConf](#omegaconf)
        - [References](#references)
        - [Evaluate](#evaluate)
        - [Singleton](#singleton)
    - [Launcher](#launcher)
        - [Default](#default-1)
        - [Launcher Configuration](#launcher-configuration)
            - [Config Dict](#config-dict)
            - [Name](#name)
            - [List](#list)
            - [Steps](#steps)
        - [HParams](#hparams)
        - [Parser](#parser)
        - [Logging](#logging)
        - [Local](#local)
- [Examples](#examples)
    - [Manual](#manual)
    - [Custom Parser](#custom-parser)
    - [Custom FromConfig](#custom-fromconfig)
    - [Custom Launcher](#custom-launcher)
    - [Launcher Extensions](#launcher-extensions)
    - [Machine Learning](#machine-learning)
    - [Custom Hyper-Parameter Search](#custom-hyper-parameter-search)
    - [MlFlow Tracking](#mlflow-tracking)
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

```yaml
# config.yaml
model:
  _attr_: foo.Model
  learning_rate: "@params.learning_rate"

# params.yaml
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
2. Merge the dictionaries into a dictionary (`config`)
3. Instantiate the `DefaultLauncher` and call `launch(config, command)` where `command` is `model - train` ([Python Fire](https://github.com/google/python-fire) syntax).
4. The `DefaultLauncher` applies the `DefaultParser` to the `config` (it resolves references as `@params.learning_rate`, etc.)
5. Finally, the `DefaultLauncher` runs the `LocalLauncher`. It recursively instantiate sub-dictionaries, using the `_attr_` key to resolve the Python class / function as an import string. It then launches `fire.Fire(object, command)`, which translates into "get the `model` key from the instantiated dictionary and execute the `train` method".

This example can be found in [`docs/examples/quickstart`](docs/examples/quickstart).

To learn more about `FromConfig` features, see the [Usage Reference](#usage-reference) and [Examples](#examples) sections.


<a id="cheat-sheet"></a>
## Cheat Sheet

`fromconfig.fromconfig` special keys


| Key        | Value Example       | Use                                               |
|------------|---------------------|---------------------------------------------------|
| `"_attr_"` | `"foo.bar.MyClass"` | Full import string of a class, function or method |
| `"_args_"` | `[1, 2]`            | Positional arguments                              |

`fromconfig.parser.DefaultParser` syntax

| Key             | Value                             | Use                                    |
|-----------------|-----------------------------------|----------------------------------------|
| `"_singleton_"` | `"my_singleton_name"`             | Creates a singleton identified by name |
| `"_eval_"`      | `"call"`, `"import"`, `"partial"` | Evaluation modes                       |
|                 | `"@params.model"`                 | Reference                              |
|                 | `"${params.url}:${params.port}"`  | Interpolation via OmegaConf            |

`fromconfig.parser.DefaultLauncher` options (keys at config's toplevel)


| Key         | Value Example                                      | Use                                         |
|-------------|----------------------------------------------------|---------------------------------------------|
| `"logging"` | `{"level": 20}`                                    | Change logging level to 20 (`logging.INFO`) |
| `"parser"`  | `{"_attr_": "fromconfig.parser.DefaultParser"}`    | Configure which parser is used              |
| `"hparams"` | `{"learning_rate": [0.1, 0.001]}`                  | Hyper-parameter search (use references like `@hparams.learning_rate` in other parts of the config)             |


Config sample

```yaml
# Configure model
model:
  _attr_: foo.Model  # Full import string to the class to instantiate
  _args_: ["@hparams.dim"]  # Positional arguments
  _singleton_: "model_${hparams.dim}_${hparams.learning_rate}"  # All @model references will instantiate the same object with that name
  _eval_: "call"  # Optional ("call" is the default behavior)
  learning_rate: "@hparams.learning_rate"  # Other key value parameter

# Configure hyper parameters, use references @hparams.key to use them
hparams:
  learning_rate: [0.1, 0.001]
  dim: [10, 100]

# Configure logging level (set to logging.INFO)
logging:
  level: 20

# Configure parser (optional, using this parser is the default behavior)
parser:
  _attr_: "fromconfig.parser.DefaultParser"

# Configure launcher (optional, the following config creates the same launcher as the default behavior)
launcher:
  sweep: "hparams"
  parse: "parser"
  log: "logging"
  run: "local"

```

for module

```python
class Model:
    def __init__(self, dim: int, learning_rate: float):
        self.dim = dim
        self.learning_rate = learning_rate

    def train(self):
        print(f"Training model({self.dim}) with learning_rate {self.learning_rate}")
```

Launch with

```bash
fromconfig config.yaml - model - train
```

This example can be found in [`docs/examples/cheat_sheet`](docs/examples/cheat_sheet).


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

The `fromconfig` library relies on three components.

1. A independent and lightweight __syntax__ to instantiate any Python object from dictionaries with `fromconfig.fromconfig(config)` (using special keys `_attr_` and `_args_`) (see [Config Syntax](#config-syntax)).
2. A composable, flexible, and customizable framework to manipulate configs and launch jobs on remote servers, log values to tracking platforms, etc. (see [Launcher](#launcher)).
3. A simple abstraction to parse configs before instantiation. This allows configs to remain short and readable with syntactic sugar to define singletons, perform interpolation, etc. (see [Parser](#parsing)).

<a id="command-line"></a>
### Command Line

Usage : call `fromconfig` on any number of paths to config files, with optional key value overrides. Use the full expressiveness of python Fire to manipulate the resulting instantiated object.

```bash
fromconfig config.yaml params.yaml --key=value - name
```

Supported formats : YAML, JSON, and [JSONNET](https://jsonnet.org).

The command line loads the different config files into Python dictionaries and merge them (if there is any key conflict, the config on the right overrides the ones from the left).

It then instantiate the `launcher` (using the `launcher` key if present in the config) and launches the config with the rest of the fire command.

With [Python Fire](https://github.com/google/python-fire), you can manipulate the resulting instantiated dictionary via the command line by using the fire syntax.

For example `fromconfig config.yaml - name` instantiates the dictionary defined in `config.yaml` and gets the value associated with the key `name`.


<a id="overrides"></a>
### Overrides

You can provide additional key value parameters following the [Python Fire](https://github.com/google/python-fire) syntax as overrides directly via the command line.

For example

```bash
fromconfig config.yaml params.yaml --params.learning_rate=0.01 - model - train
```
will print

```
Training model with learning_rate 0.01
```

This is strictly equivalent to defining another config file (eg. `overrides.yaml`)

```yaml
params:
    learning_rate: 0.01
```

and running

```bash
fromconfig config.yaml params.yaml overrides.yaml - model - train
```

since the config files are merged from left to right, the files on the right overriding the existing keys from the left in case of conflict.

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

- `OmegaConfParser`: can be practical for interpolation ([learn more](#omegaconf))
- `ReferenceParser`: resolves references ([learn more](#references))
- `EvaluateParser`: syntactic sugar to configure `functool.partial` or simple imports ([learn more](#evaluate))
- `SingletonParser`: syntactic sugar to define singletons ([learn more](#singletons))

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
```

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


<a id="launcher"></a>
### Launcher

<a id="default-1"></a>
#### Default

When a `fromconfig` command is executed (example `fromconfig config.yaml params.yaml - model - train`), the config is loaded, a launcher is instantiated (possibly configured by the config itself) and then the launcher "launches" the config with the remaining fire arguments.

By default, 4 launchers are executed in the following order

- `fromconfig.launcher.HParamsLauncher`: uses the `hparams` key of the config (if present) to launch multiple sub-configs from a grid of hyper-parameters ([learn more](#hparams))
- `fromconfig.launcher.Parser`: applies a parser (by default, `DefaultParser`) to the config to replace references etc. ([learn more](#parser))
- `fromconfig.launcher.LoggingLauncher`: uses `logging.info` to log a flattened view of the config ([learn more](#logging))
- `fromconfig.launcher.LocalLauncher`: runs `fire.Fire(fromconfig.fromconfig(config), command)` to instantiate and execute the config with the fire arguments (`command`, for example `model - train`) ([learn more](#local)).

Let's see for example how to configure the logging level and perform an hyper-parameter search.

Given the following module and config files (similar to the quickstart, we only changed `params` into `hparams`)

```python
class Model:
    def __init__(self, learning_rate: float):
        self.learning_rate = learning_rate

    def train(self):
        print(f"Training model with learning_rate {self.learning_rate}")
```

```yaml
# config.yaml
model:
  _attr_: foo.Model
  learning_rate: "@hparams.learning_rate"

# params.yaml
hparams:
  learning_rate: [0.01, 0.001]

# launcher.yaml
logging:
  level: 20
```

run

```bash
fromconfig config.yaml params.yaml launcher.yaml - model - train
```

You should see plenty of logs and two trainings

```
INFO:fromconfig.launcher.logger:- model._attr_: foo.Model
INFO:fromconfig.launcher.logger:- model.learning_rate: 0.01
....
Training model with learning_rate 0.01
INFO:fromconfig.launcher.logger:- model._attr_: foo.Model
INFO:fromconfig.launcher.logger:- model.learning_rate: 0.001
...
Training model with learning_rate 0.001
```

<a id="launcher-configuration"></a>
#### Launcher Configuration

The launcher is instantiated from the `launcher` key if present in the config.

For ease of use, multiple syntaxes are provided.

<a id="config-dict"></a>
##### Config Dict
The `launcher` entry can be a config dictionary (with an `_attr_` key) that defines how to instantiate a `Launcher` instance (possibly custom).

For example

```yaml
launcher:
    _attr_: fromconfig.launcher.LocalLauncher
```

<a id="name"></a>
##### Name
The `launcher` entry can be a `str`, corresponding to a name that maps to a `Launcher` class. The internal `Launcher` names are


| Name    | Class                                 |
|---------|---------------------------------------|
| hparams | `fromconfig.launcher.HParamsLauncher` |
| parser  | `fromconfig.launcher.ParserLauncher`  |
| logging | `fromconfig.launcher.LoggingLauncher` |
| local   | `fromconfig.launcher.LocalLauncher`   |

It is possible via extensions to add new `Launcher` classes to the list of available launchers (learn more in the examples section).


<a id="list"></a>
##### List
The `launcher` entry can be a list of [config dict](#config-dict) and/or [names](#name). In that case, the resulting launcher is a nested launcher instance of the different launchers.

For example

```yaml
launcher:
    - hparams
    - local
```

will result in `HParamsLauncher(LocalLauncher())`.


<a id="steps"></a>
##### Steps
The `launcher` entry can also be a dictionary with 4 special keys for which the value can be any of config dict, name or list.

- `sweep`: if not specified, will use [`hparams`](#hparams)
- `parse`: if not specified, will use [`parser`](#parser)
- `log`: if not specified, will use [`logging`](#logging)
- `run`: if not specified, will use [`local`](#logging)

Setting either all or a subset of these keys allows you to modify one of the 4 steps while still using the defaults for the rest of the steps.

The result, again, is similar to the list mechanism, as a nested instance.

For example

```yaml
launcher:
  sweep: hparams
  parse: parser
  log: logging
  run: local
```

results in `HParamsLauncher(ParserLauncher(LoggingLauncher(LocalLauncher())))`.


<a id="hparams"></a>
#### HParams

The `HParamsLauncher` provides basic hyper parameter search support. It is active by default.

In your config, simply add a `hparams` entry. Each key is the name of a hyper parameter. Each value should be an iterable of values to try. The `HParamsLauncher` retrieves these hyper-parameter values, iterates over the combinations (Cartesian product) and launches each config overriding the `hparams` entry with the actual values.

For example

```yaml
fromconfig --hparams.a=1,2 --hparams.b=3,4
```

Generates

```
hparams: {"a": 1, "b": 3}
hparams: {"a": 1, "b": 4}
hparams: {"a": 2, "b": 3}
hparams: {"a": 2, "b": 4}
```

<a id="parser"></a>
#### Parser

The `ParserLauncher` applies parsing to the config. By default, it uses the `DefaultParser`. You can configure the parser with your custom parser by overriding the `parser` key of the config.

For example

```yaml
parser:
    _attr_: "fromconfig.parser.DefaultParser"
```

Will tell the `ParserLauncher` to instantiate the `DefaultParser`.

<a id="logging"></a>
#### Logging

The `LoggingLauncher` can change the logging level (modifying the `logging.basicConfig` so this will apply to any other `logger` configured to impact the logging's root logger) and log a flattened view of the parameters.

For example, to change the logging verbosity to `INFO` (20), simply do

```yaml
logging:
    level: 20
```


<a id="local"></a>
#### Local

The previous `Launcher`s were only either generating configs, parsing them, or logging them. To actually instantiate the object using `fromconfig` and manipulate the resulting object via the python Fire syntax, the default behavior is to use the `LocalLauncher`.

If you wanted to execute the code remotely, you would have to swap the `LocalLauncher` by your custom `Launcher`.

<a id="examples"></a>
## Examples

Note: you can run all the examples with `make examples` (see [Makefile](./Makefile)).

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


<a id="custom-launcher"></a>
### Custom Launcher

Another flexibility provided by `fromconfig` is the ability to write custom `Launcher` classes.

The `Launcher` base class is simple

```python
class Launcher(FromConfig, ABC):
    """Base class for launchers."""

    def __init__(self, launcher: "Launcher"):
        self.launcher = launcher

    def __call__(self, config: Any, command: str = ""):
        """Launch implementation.

        Parameters
        ----------
        config : Any
            The config
        command : str, optional
            The fire command
        """
        raise NotImplementedError()
```

For example, let's implement a `Launcher` that simply prints the command (and does nothing else).

```python
from typing import Any

import fromconfig


class PrintCommandLauncher(fromconfig.launcher.Launcher):
    def __call__(self, config: Any, command: str = ""):
        print(command)
        self.launcher(config=config, command=command)
```

Given the following launcher config

```yaml
# config.yaml
model:
  _attr_: foo.Model
  learning_rate: 0.1

# launcher.yaml
launcher:
  log:
    _attr_: print_command.PrintCommandLauncher
```

and module

```python
# foo.py
class Model:
    def __init__(self, learning_rate: float):
        self.learning_rate = learning_rate

    def train(self):
        print(f"Training model with learning_rate {self.learning_rate}")
```

Run

```
fromconfig config.yaml launcher.yaml - model - train
```

You should see

```
model - train
Training model with learning_rate 0.1
```

This example can be found in [`docs/examples/custom_launcher`](docs/examples/custom_launcher).


<a id="launcher-extensions"></a>
### Launcher Extensions

Once you've implemented your custom launcher (it usually fits one of the `sweep`, `parse`, `log`, `run` steps), you can share it as a `fromconfig` extension.

To do so, publish a new package on `PyPI` that has a specific entry point that maps to a module defined in your package in which one `Launcher` class is defined.

To add an entry point, update the `setup.py` by adding

```python
setuptools.setup(
    ...
    entry_points={"fromconfig0": ["your_extension_name = your_extension_module"]},
)
```

Make sure to look at the available launchers defined directly in `fromconfig`. It is recommended to keep the number of `__init__` arguments as low as possible (if any) and instead retrieve parameters from the `config` itself at run time. A good practice is to use the same name for the config entry that will be used as the shortened name given by the entry-point.

If your `Launcher` class is not meant to wrap another `Launcher` class (that's the case of the `LocalLauncher` for example), make sure to override the `__init__` method like so

```python
def __init__(self, launcher: Launcher = None):
    if launcher is not None:
        raise ValueError(f"Cannot wrap another launcher but got {launcher}")
    super().__init__(launcher=launcher)  # type: ignore
```

An example can be found in [`docs/examples/launcher_yarn_mlflow`](docs/examples/launcher_yarn_mlflow), using two extensions

- [`fromconfig-mlflow`](https://github.com/guillaumegenthial/fromconfig-mlflow): tracking support with [MlFlow](https://www.mlflow.org)
- [`fromconfig-yarn`](https://github.com/criteo/fromconfig-yarn): execution on a yarn cluster using [cluster-pack](https://github.com/criteo/cluster-pack)

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

This example can be found in [`docs/examples/ml`](docs/examples/ml).

Note that it is encouraged to save these config files with the experiment's files to get full reproducibility. [MlFlow](https://mlflow.org) is an open-source platform that tracks your experiments by logging metrics and artifacts.


<a id="custom-hyper-parameter-search"></a>
### Custom Hyper-Parameter Search

You can use the `hparams` entry, that the `HParamsLauncher` uses to generate configs (see [more above](#hparams)).

Reusing the [ML example](#machine-learning), simply add a `hparams.yaml` file

```yaml
params:
  dim: "@hparams.dim"
  learning_rate: "@hparams.learning_rate"

hparams:
  dim: [10, 100]
  learning_rate: [0.1, 0.01]
```

And launch a hyper-parameter sweep with

```bash
fromconfig trainer.yaml model.yaml optimizer.yaml hparams.yaml - trainer - run
```

which should print

```
Training Model(dim=10) with Optimizer(learning_rate=0.1)
Training Model(dim=10) with Optimizer(learning_rate=0.01)
Training Model(dim=100) with Optimizer(learning_rate=0.1)
Training Model(dim=100) with Optimizer(learning_rate=0.01)
```

You can also write your custom config generator (and even make it a `Launcher`, see [how to implement a custom Launcher](#custom-launcher)).

For example, something that is equivalent to what we just did is

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
            # Clear the singletons if any as we most likely don't want
            # to share between configs
            fromconfig.parser.singleton.clear()
```

which prints

```
Training Model(dim=10) with Optimizer(learning_rate=0.01)
Training Model(dim=10) with Optimizer(learning_rate=0.1)
Training Model(dim=100) with Optimizer(learning_rate=0.01)
Training Model(dim=100) with Optimizer(learning_rate=0.1)
```

This example can be found in [`docs/examples/ml`](docs/examples/ml) (run `python hp.py`).


<a id="mlflow-tracking"></a>
### MlFlow Tracking

[MlFlow](https://www.mlflow.org) is an open-source platform for the Machine Learning life-cycle.

To install an launch an MlFlow server

```bash
pip install mlflow
mlflow server --port 5000
```

Once the server is up, you can register new runs and log parameters, metrics, and artifacts. Saving the metrics as a run's artifact is a good way to ensure future reproducibility.

A custom command equivalent to `fromconfig` with MlFlow support would look like

```python
import sys
import functools
import logging
import tempfile
import json
from pathlib import Path

import mlflow
import fire
import fromconfig


LOGGER = logging.getLogger(__name__)


def main(
    *paths: str,
    use_mlflow: bool = False,
    run_name: str = None,
    run_id: str = None,
    tracking_uri: str = None,
    experiment_name: str = None,
    artifact_location: str = None,
):
    """Command line with MlFlow support."""
    if not paths:
        return main

    # Load configs and merge them
    configs = [fromconfig.load(path) for path in paths]
    config = functools.reduce(fromconfig.utils.merge_dict, configs)

    # Parse merged config
    parser = fromconfig.parser.DefaultParser()
    parsed = parser(config)

    if use_mlflow:  # Create run, log configs and parameters
        # Configure MlFlow
        if tracking_uri is not None:
            mlflow.set_tracking_uri(tracking_uri)
        if experiment_name is not None:
            if mlflow.get_experiment_by_name(experiment_name) is None:
                mlflow.create_experiment(name=experiment_name, artifact_location=artifact_location)
            mlflow.set_experiment(experiment_name)

        # Start run (cannot use context because of python Fire)
        run = mlflow.start_run(run_id=run_id, run_name=run_name)

        # Log run information
        url = f"{mlflow.get_tracking_uri()}/#/experiments/{run.info.experiment_id}/runs/{run.info.run_id}"
        LOGGER.info(f"MlFlow Run Initialized: {url}")

        # Save merged and parsed config to MlFlow
        dir_artifacts = tempfile.mkdtemp()
        with Path(dir_artifacts, "config.json").open("w") as file:
            json.dump(config, file, indent=4)
        with Path(dir_artifacts, "parsed.json").open("w") as file:
            json.dump(parsed, file, indent=4)
        mlflow.log_artifacts(local_dir=dir_artifacts)

        # Log flattened parameters
        for key, value in fromconfig.utils.flatten(parsed):
            mlflow.log_param(key=key, value=value)

    return fromconfig.fromconfig(parsed)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)  # Print INFO level logs
    sys.path.append(".")  # For local imports
    fire.Fire(main)
```

This example can be found in [`docs/examples/mlflow`](docs/examples/mlflow).

Start an MlFlow server with

```bash
mlflow server --port 5000
```

And submit an experiment with

```bash
python submit.py config.yaml params.yaml \
    --use_mlflow=True \
    --tracking_uri='http://127.0.0.1:5000' \
    --run_name='test' \
    - model - train
```

This should print

```
INFO:__main__:MlFlow Run Initialized: http://127.0.0.1:5000/#/experiments/0/runs/<SOME RUN ID>
Training model with learning_rate 0.1
```

Navigate to the URL to inspect the run's outputs (parameters, configs, metrics, etc.)

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

To run tests

```bash
make test
```
