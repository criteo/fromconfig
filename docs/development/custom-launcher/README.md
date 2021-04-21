# Custom Launcher <!-- {docsify-ignore} -->

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

[print_command.py](print_command.py ':include :type=code python')

Given the following config files

`config.yaml`

[config.yaml](config.yaml ':include :type=code yaml')

`launcher.yaml`

[launcher.yaml](launcher.yaml ':include :type=code yaml')

and module `model.py`


[model.py](model.py ':include :type=code python')

Run

```
fromconfig config.yaml launcher.yaml - model - train
```

You should see

```
model - train
Training model with learning_rate 0.1
```
