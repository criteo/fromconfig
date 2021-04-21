# Custom FromConfig  <!-- {docsify-ignore} -->

The logic to instantiate objects from config dictionaries is always the same.

It resolves the class, function or method `attr` from the `_attr_` key, recursively call `fromconfig` on all the other key-values to get a `kwargs` dictionary of objects, and call `attr(**kwargs)`.

It is possible to customize the behavior of `fromconfig` by inheriting the `FromConfig` class.

For example

[custom.py](custom.py ':include :type=code python')


One custom `FromConfig` class is provided in `fromconfig` which makes it possible to stop the instantiation and keep config dictionaries as config dictionaries.

For example

[config.py](config.py ':include :type=code python')
