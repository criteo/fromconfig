### Custom FromConfig  <!-- {docsify-ignore} -->

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
