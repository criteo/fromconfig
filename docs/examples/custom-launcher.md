### Custom Launcher <!-- {docsify-ignore} -->

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

This example can be found in [`examples/custom_launcher`](examples/custom_launcher).
