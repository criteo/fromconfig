### Custom Parser <!-- {docsify-ignore} -->

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

This example can be found in [`examples/custom_parser`](examples/custom_parser)
