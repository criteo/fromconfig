# FromConfig


## Install

```bash
pip install fromconfig
```

## Quickstart

```python
from fromconfig import fromconfig


class Model:
    """Custom Model defined in current module."""

    def __init__(self, dim: int):
        self.dim = dim


config = {
    "_attr_": "__main__.Model",
    "dim": 100
}
model = fromconfig(config)
```
