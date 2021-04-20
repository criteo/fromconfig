### Parser <!-- {docsify-ignore} -->

<a id="default"></a>
#### Default

`FromConfig` comes with a default parser which sequentially applies

- `OmegaConfParser`: can be practical for interpolation ([learn more](#omegaconf))
- `ReferenceParser`: resolves references ([learn more](#references))
- `EvaluateParser`: syntactic sugar to configure `functool.partial` or simple imports ([learn more](#evaluate))
- `SingletonParser`: syntactic sugar to define singletons ([learn more](#singleton))

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
