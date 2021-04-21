# Publish Extensions <!-- {docsify-ignore} -->

Once you've implemented a custom [`Launcher`](#usage-reference/launcher/), you can share it as a `fromconfig` extension.

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

Once your extension is available, update `fromconfig` documentation and add an example in [extensions](extensions).
