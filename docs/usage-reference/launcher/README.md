# Launcher <!-- {docsify-ignore} -->

<a id="default-1"></a>
## Default

When a `fromconfig` command is executed (example `fromconfig config.yaml params.yaml - model - train`), the config is loaded, a launcher is instantiated (possibly configured by the config itself if the `launcher` key is present in the config) and then the launcher "launches" the config with the remaining fire arguments.

By default, 4 launchers are executed in the following order

- [`fromconfig.launcher.HParamsLauncher`](#hparams): uses the `hparams` key of the config (if present) to launch multiple sub-configs from a grid of hyper-parameters.
- [`fromconfig.launcher.Parser`](#parser): applies a parser (by default, `DefaultParser`) to the config to resolve interpolation, singletons, etc.
- [`fromconfig.launcher.LoggingLauncher`](#logging): uses `logging.info` to log a flattened view of the config.
- [`fromconfig.launcher.LocalLauncher`](#local): runs `fire.Fire(fromconfig.fromconfig(config), command)` to instantiate and execute the config with the fire arguments (`command`, for example `model - train`).

Let's see for example how to configure the logging level and perform an hyper-parameter search.

Given the following module and config files (similar to the quickstart, we only changed `params` into `hparams`)

`model.py`

[model.py](model.py ':include :type=code python')

`config.yaml`

[config.yaml](config.yaml ':include :type=code yaml')

`hparams.yaml`

[hparams.yaml](hparams.yaml ':include :type=code yaml')


`launcher.yaml`

[launcher.yaml](launcher.yaml ':include :type=code yaml')

run

```bash
fromconfig config.yaml hparams.yaml launcher.yaml - model - train
```

You should see plenty of logs and two trainings

```
INFO:fromconfig.launcher.logger:- model._attr_: model.Model
INFO:fromconfig.launcher.logger:- model.learning_rate: 0.01
....
Training model with learning_rate 0.01
INFO:fromconfig.launcher.logger:- model._attr_: model.Model
INFO:fromconfig.launcher.logger:- model.learning_rate: 0.001
...
Training model with learning_rate 0.001
```


<a id="launcher-configuration"></a>
## Launcher Configuration

The launcher is instantiated from the `launcher` key if present in the config.

For ease of use, multiple syntaxes are provided.

<a id="config-dict"></a>
### Config Dict
The `launcher` entry can be a config dictionary (with an `_attr_` key) that defines how to instantiate a `Launcher` instance (possibly custom).

For example

```yaml
launcher:
    _attr_: fromconfig.launcher.LocalLauncher
```

<a id="name"></a>
### Name
The `launcher` entry can be a `str`, corresponding to a name that maps to a `Launcher` class. The internal `Launcher` names are


| Name    | Class                                 |
|---------|---------------------------------------|
| hparams | `fromconfig.launcher.HParamsLauncher` |
| parser  | `fromconfig.launcher.ParserLauncher`  |
| logging | `fromconfig.launcher.LoggingLauncher` |
| local   | `fromconfig.launcher.LocalLauncher`   |

It is possible via extensions to add new `Launcher` classes to the list of available launchers (learn more in the examples section).

<a id="list"></a>
### List
The `launcher` entry can be a list of [config dict](#config-dict) and/or [names](#name). In that case, the resulting launcher is a nested launcher instance of the different launchers.

For example

```yaml
launcher:
    - hparams
    - local
```

will result in `HParamsLauncher(LocalLauncher())`.

<a id="steps"></a>
### Steps
The `launcher` entry can also be a dictionary with 4 special keys for which the value can be any of config dict, name or list.

- `sweep`: if not specified, will use [`hparams`](#hparams)
- `parse`: if not specified, will use [`parser`](#parser)
- `log`: if not specified, will use [`logging`](#logging)
- `run`: if not specified, will use [`local`](#logging)

Setting either all or a subset of these keys allows you to modify one of the 4 steps while still using the defaults for the rest of the steps.

The result, again, is similar to the list mechanism, as a nested instance.

For example

```yaml
launcher:
  sweep: hparams
  parse: parser
  log: logging
  run: local
```

results in `HParamsLauncher(ParserLauncher(LoggingLauncher(LocalLauncher())))`.


<a id="hparams"></a>
## HParams

The `HParamsLauncher` provides basic hyper parameter search support. It is active by default.

In your config, simply add a `hparams` entry. Each key is the name of a hyper parameter. Each value should be an iterable of values to try. The `HParamsLauncher` retrieves these hyper-parameter values, iterates over the combinations (Cartesian product) and launches each config overriding the `hparams` entry with the actual values.

For example

```yaml
fromconfig --hparams.a=1,2 --hparams.b=3,4
```

Generates

```
hparams: {"a": 1, "b": 3}
hparams: {"a": 1, "b": 4}
hparams: {"a": 2, "b": 3}
hparams: {"a": 2, "b": 4}
```


<a id="parser"></a>
## Parser

The `ParserLauncher` applies parsing to the config. By default, it uses the `DefaultParser`. You can configure the parser with your custom parser by overriding the `parser` key of the config.

For example

```yaml
parser:
    _attr_: "fromconfig.parser.DefaultParser"
```

Will tell the `ParserLauncher` to instantiate the `DefaultParser`.

<a id="logging"></a>
## Logging

The `LoggingLauncher` can change the logging level (modifying the `logging.basicConfig` so this will apply to any other `logger` configured to impact the logging's root logger) and log a flattened view of the parameters.

For example, to change the logging verbosity to `INFO` (20), simply do

```yaml
logging:
    level: 20
```


<a id="local"></a>
## Local

The previous `Launcher`s were only either generating configs, parsing them, or logging them. To actually instantiate the object using `fromconfig` and manipulate the resulting object via the python Fire syntax, the default behavior is to use the `LocalLauncher`.

If you wanted to execute the code remotely, you would have to swap the `LocalLauncher` by your custom `Launcher`.
