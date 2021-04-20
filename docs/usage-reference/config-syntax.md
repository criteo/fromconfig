The `fromconfig` library relies on three components.

1. A independent and lightweight __syntax__ to instantiate any Python object from dictionaries with `fromconfig.fromconfig(config)` (using special keys `_attr_` and `_args_`) (see [Config Syntax](usage-reference/config-syntax)).
2. A composable, flexible, and customizable framework to manipulate configs and launch jobs on remote servers, log values to tracking platforms, etc. (see [Launcher](usage-reference/launcher)).
3. A simple abstraction to parse configs before instantiation. This allows configs to remain short and readable with syntactic sugar to define singletons, perform interpolation, etc. (see [Parser](usage-reference/parser)).


### Config syntax <!-- {docsify-ignore} -->

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
