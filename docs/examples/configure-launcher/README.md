# Configure Launcher <!-- {docsify-ignore} -->

The easiest way to configure the launcher is to change one of the 4 steps.

The default is configured in the following way

[launcher_default.yaml](launcher_default.yaml ':include :type=code yaml')

## Dry run

Let's see how to swap the `LocalLauncher` (configured by `run: local`) with the `DryLauncher` (configured by `run: dry`).

For example, given the following module and config file

`model.py`

[model.py](model.py ':include :type=code python')

`config.yaml`

[config.yaml](config.yaml ':include :type=code yaml')

run

```bash
fromconfig config.yaml --launcher.run=dry - model - train
```

which prints the config and command but does not instantiate or run any method.

```
{'model': {'_attr_': 'model.Model', 'learning_rate': 0.1}}
model - train
```

Note that it is equivalent to adding a `launcher_dry.yaml` config file

[launcher_dry.yaml](launcher_dry.yaml ':include :type=code yaml')

and running

```bash
fromconfig config.yaml launcher_dry.yaml - model - train
```

## Configure Logging

The logging launcher (responsible for basic logging, configured by `log: logging`) can be configured with the `logging.level` parameter.

For example,

```bash
fromconfig config.yaml --logging.level=20 - model - train
```

prints

```
INFO:model:Training model with learning_rate 0.1
```

Note that this is equivalent to adding a `launcher_logging.yaml` config file

[launcher_logging.yaml](launcher_logging.yaml ':include :type=code yaml')

and running

```bash
fromconfig config.yaml launcher_logging.yaml - model - train
```

## Advanced

It is also possible to use a [custom launcher](development/custom-launcher/) and / or [customize how the different launchers are composed](usage-reference/launcher/).
