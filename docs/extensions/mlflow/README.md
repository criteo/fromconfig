# FromConfig MlFlow <!-- {docsify-ignore} -->
[![pypi](https://img.shields.io/pypi/v/fromconfig-mlflow.svg)](https://pypi.python.org/pypi/fromconfig-mlflow)
[![ci](https://github.com/criteo/fromconfig-mlflow/workflows/Continuous%20integration/badge.svg)](https://github.com/criteo/fromconfig-mlflow/actions?query=workflow%3A%22Continuous+integration%22)

A [fromconfig](https://github.com/criteo/fromconfig) `Launcher` for [MlFlow](https://www.mlflow.org) support.


## Install

```bash
pip install fromconfig_mlflow
```

<a id="quickstart"></a>
## Quickstart

To activate `MlFlow` login, simply add `--launcher.log=mlflow` to your command

```bash
fromconfig config.yaml params.yaml --launcher.log=mlflow - model - train
```

### Configure the MlFlow tracking URI

To setup a local MlFlow tracking server, run

```bash
mlflow server
```

which should print

```
[INFO] Starting gunicorn 20.0.4
[INFO] Listening at: http://127.0.0.1:5000
```

We will assume that the tracking URI is `http://127.0.0.1:5000` from now on.

Set the `MLFLOW_TRACKING_URI` environment variable

```bash
export MLFLOW_TRACKING_URI=http://127.0.0.1:5000
```

### Configs

Given the following module `model.py`

[model.py](model.py ':include :type=code python')

and config files

`config.yaml`

[config.yaml](config.yaml ':include :type=code yaml')

`params.yaml`

[params.yaml](params.yaml ':include :type=code yaml')

Run

```bash
fromconfig config.yaml params.yaml --launcher.log=mlflow - model - train
```

which prints

```
Started run: http://127.0.0.1:5000/experiments/0/runs/7fe650dd99574784aec1e4b18fceb73f
Training model with learning_rate 0.001
```

If you navigate to `http://127.0.0.1:5000/experiments/0/runs/7fe650dd99574784aec1e4b18fceb73f` you should see your parameters and configs.

### Using a `launcher.yaml` file

You can also use a `launcher.yaml` file

`launcher.yaml`

[launcher.yaml](launcher.yaml ':include :type=code yaml')

Run

```bash
fromconfig config.yaml params.yaml launcher.yaml - model - train
```

<a id="multi"></a>
## Advanced

In this example, we show how to call and configure multiple launches of the `MlFlowLauncher`.

We first log the non-parsed configs, then parse, then log both the parsed configs and the flattened parameters.

Re-using the [quickstart](#quickstart) code, modify the `launcher.yaml` file

[launcher_advanced.yaml](launcher_advanced.yaml ':include :type=code yaml')

and run

```bash
fromconfig config.yaml params.yaml launcher_advanced.yaml - model - train
```

which prints

```
INFO:fromconfig_mlflow.launcher:Started run: http://127.0.0.1:5000/experiments/0/runs/<MLFLOW_RUN_ID>
INFO:fromconfig_mlflow.launcher:Logging artifacts config.yaml and config_launch.sh
INFO:fromconfig.launcher.parser:Resolved parser DefaultParser
INFO:fromconfig_mlflow.launcher:Active run found: http://127.0.0.1:5000/experiments/0/runs/<MLFLOW_RUN_ID>
INFO:fromconfig_mlflow.launcher:Logging artifacts parsed.yaml and parse_launch.sh
INFO:fromconfig_mlflow.launcher:Logging parameters
Training model with learning_rate 0.001
```

If you navigate to the MlFlow run, you should see
- the parameters, a flattened version of the *parsed* config (`model.learning_rate` is `0.001` and not `${params.learning_rate}`)
- the original config, saved as `config.yaml`
- the parsed config, saved as `parsed.yaml`

Note that we run the logger in different steps, before parsing and after parsing.

<a id="options"></a>
## Options
To configure MlFlow, add a `mlflow` entry to your config and set the following parameters

- `run_id`: if you wish to restart an existing run
- `run_name`: if you wish to give a name to your new run
- `tracking_uri`: to configure the tracking remote
- `experiment_name`: to use a different experiment than the custom
  experiment
- `artifact_location`: the location of the artifacts (config files)

You can also set the following attributes

- `log_artifacts` : If True, save config and command as artifacts.
- `log_parameters` : If True, log flattened config as parameters.
- `path_command` : Name for the command file
- `path_config` : Name for the config file.
- `set_env_vars` : If True, set MlFlow environment variables.
- `set_run_id` : If True, the run_id is overridden in the config.
- `ignore_keys` : If given, don't log some parameters that have some substrings.
- `include_keys` : If given, only log some parameters that have some substrings. Also shorten the flattened parameter to start at the first match. For example, if the config is `{"foo": {"bar": 1}}` and `include_keys=("bar",)`, then the logged parameter will be `("bar", 1)`.
