# FromConfig MlFlow <!-- {docsify-ignore} -->
[![pypi](https://img.shields.io/pypi/v/fromconfig-mlflow.svg)](https://pypi.python.org/pypi/fromconfig-mlflow)
[![ci](https://github.com/criteo/fromconfig-mlflow/workflows/Continuous%20integration/badge.svg)](https://github.com/criteo/fromconfig-mlflow/actions?query=workflow%3A%22Continuous+integration%22)

A [fromconfig](https://github.com/criteo/fromconfig) `Launcher` for [MlFlow](https://www.mlflow.org) support.


<a id="install"></a>
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

With

`model.py`

[model.py](model.py ':include :type=code python')

`config.yaml`

[config.yaml](config.yaml ':include :type=code yaml')

`params.yaml`

[params.yaml](params.yaml ':include :type=code yaml')


It should print

```
Started run: http://127.0.0.1:5000/experiments/0/runs/7fe650dd99574784aec1e4b18fceb73f
Training model with learning_rate 0.001
```

If you navigate to `http://127.0.0.1:5000/experiments/0/runs/7fe650dd99574784aec1e4b18fceb73f` you should see the logged `learning_rate` metric.

<a id="mlflow-server"></a>
## MlFlow server

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


<a id="configure-mlflow"></a>
## Configure MlFlow

You can set the tracking URI either via an environment variable or via the config.

To set the `MLFLOW_TRACKING_URI` environment variable

```bash
export MLFLOW_TRACKING_URI=http://127.0.0.1:5000
```

Alternatively, you can set the `mlflow.tracking_uri` config key either via command line with

```bash
fromconfig config.yaml params.yaml --launcher.log=mlflow --mlflow.tracking_uri="http://127.0.0.1:5000" - model - train
```

or in a config file with

`launcher.yaml`

[launcher.yaml](launcher.yaml ':include :type=code yaml')

and run

```bash
fromconfig config.yaml params.yaml launcher.yaml - model - train
```

<a id="artifacts-and-parameters"></a>
## Artifacts and Parameters

In this example, we add logging of the config and parameters.

Re-using the [quickstart](#quickstart) code, modify the `launcher.yaml` file

[launcher_artifacts_params.yaml](launcher_artifacts_params.yaml ':include :type=code yaml')

and run

```bash
fromconfig config.yaml params.yaml launcher.yaml - model - train
```

which prints

```
INFO:fromconfig_mlflow.launcher:Started run: http://127.0.0.1:5000/experiments/0/runs/<MLFLOW_RUN_ID>
Training model with learning_rate 0.001
```

If you navigate to the MlFlow run URL, you should see
- the original config, saved as `config.yaml`
- the parameters, a flattened version of the *parsed* config (`model.learning_rate` is `0.001` and not `${params.learning_rate}`)


<a id="usage-reference"></a>
## Usage-Reference

<a id="startrunlauncher"></a>
### `StartRunLauncher`

To configure MlFlow, add a `mlflow` entry to your config and set the following parameters

- `run_id`: if you wish to restart an existing run
- `run_name`: if you wish to give a name to your new run
- `tracking_uri`: to configure the tracking remote
- `experiment_name`: to use a different experiment than the custom
  experiment
- `artifact_location`: the location of the artifacts (config files)

Additionally, the launcher can be initialized with the following attributes

- `set_env_vars`: if True (default is `True`), set `MLFLOW_RUN_ID` and `MLFLOW_TRACKING_URI`
- `set_run_id`: if True (default is `False`), set `mlflow.run_id` in config.

For example,

[launcher_start.yaml](launcher_start.yaml ':include :type=code yaml')


<a id="logartifactslauncher"></a>
### `LogArtifactsLauncher`

The launcher can be initialized with the following attributes

- `path_command`: Name for the command file. If `None`, don't log the command.
- `path_config`: Name for the config file. If `None`, don't log the config.

For example,

[launcher_artifacts.yaml](launcher_artifacts.yaml ':include :type=code yaml')


<a id="logparamslauncher"></a>
### `LogParamsLauncher`

The launcher will use `include_keys` and `ignore_keys`  if present in the config in the `mlflow` key.

- `ignore_keys` : If given, don't log some parameters that have some substrings.
- `include_keys` : If given, only log some parameters that have some substrings. Also shorten the flattened parameter to start at the first match. For example, if the config is `{"foo": {"bar": 1}}` and `include_keys=("bar",)`, then the logged parameter will be `"bar"`.

For example,

[launcher_params.yaml](launcher_params.yaml ':include :type=code yaml')
