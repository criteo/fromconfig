# Config syntax <!-- {docsify-ignore} -->

The `fromconfig.fromconfig` function recursively instantiates objects from dictionaries.

It uses two special keys

- `_attr_`: (optional) full import string to any Python object.
- `_args_`: (optional) positional arguments.

For example,

[example.py](example.py ':include :type=code python')

`FromConfig` resolves the builtin type `str` from the `_attr_` key, and creates a new string with the positional arguments defined in `_args_`, in other words `str(1)` which return `'1'`.

If the `_attr_` key is not given, then the dictionary is left as a dictionary (the values of the dictionary may be recursively instantiated).

If other keys are available in the dictionary, they are treated as key-value arguments (`kwargs`).

For example

[example_kwargs.py](example_kwargs.py ':include :type=code python')

Note that any mapping-like container is supported (there is no special "config" class in `fromconfig`).
