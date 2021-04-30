# Publish Extensions <!-- {docsify-ignore} -->

## Discovery

Once you've implemented a custom [`Launcher`](#usage-reference/launcher/), you can share it as a `fromconfig` extension.

To do so, publish a new package on `PyPI` that has a specific entry point that maps to a module defined in your package in which one or more `Launcher` classes is defined.

To add an entry point, update the `setup.py` by adding

```python
setuptools.setup(
    ...
    entry_points={"fromconfig0": ["your_extension_name = your_extension_module"]},
)
```

Each `Launcher` class defined in the entry-point can define a class attribute `NAME` that uniquely identifies the launcher.

For example, if the entry point name (`your_extension_name`) is `debug`, the following launcher will be available under the name `debug.print_command`.

```python
"""Custom Launcher that prints the command."""

from typing import Any

import fromconfig


class PrintCommandLauncher(fromconfig.launcher.Launcher):

    NAME = "print_command"

    def __call__(self, config: Any, command: str = ""):
        print(command)
        # Launcher are nested by default
        self.launcher(config=config, command=command)
```


If you don't specify the `NAME` attribute, the entry point name will be used.

If your extension implements more than one launcher, you need to specify the `NAME` of each `Launcher` class (except one) otherwise there will be a name conflict.


## Implementation

Make sure to look at the available launchers defined directly in `fromconfig`.

It is recommended to keep the number of `__init__` arguments as low as possible (if any) and instead retrieve parameters from the `config` itself at run time. A rule of thumb is to use `__init__` arguments only if the launcher is meant to be called multiple times with different options.

If your `Launcher` class is not meant to wrap another `Launcher` class (that's the case of the `LocalLauncher` for example), make sure to override the `__init__` method like so

```python
def __init__(self, launcher: Launcher = None):
    if launcher is not None:
        raise ValueError(f"Cannot wrap another launcher but got {launcher}")
    super().__init__(launcher=launcher)  # type: ignore
```

Once your extension is available, update `fromconfig` documentation and add an example in [extensions](extensions/).
