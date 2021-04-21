# FromConfig MlFlow <!-- {docsify-ignore} -->
[![pypi](https://img.shields.io/pypi/v/fromconfig-mlflow.svg)](https://pypi.python.org/pypi/fromconfig-mlflow)
[![ci](https://github.com/guillaumegenthial/fromconfig-mlflow/workflows/Continuous%20integration/badge.svg)](https://github.com/guillaumegenthial/fromconfig-mlflow/actions?query=workflow%3A%22Continuous+integration%22)

A [fromconfig](https://github.com/criteo/fromconfig) `Launcher` for [MlFlow](https://www.mlflow.org) support.


## Install

```bash
pip install fromconfig_mlflow
```

<a id="quickstart"></a>
## Quickstart

Once installed, the launcher is available with the name `mlflow`.

Start a local MlFlow server with

```bash
mlflow server
```

You should see

```
[INFO] Starting gunicorn 20.0.4
[INFO] Listening at: http://127.0.0.1:5000
```

We will assume that the tracking URI is `http://127.0.0.1:5000` from now on.

Given the following module `model.py`

[model.py](model.py ':include :type=code python')

and config files

`config.yaml`

[config.yaml](config.yaml ':include :type=code yaml')

`params.yaml`

[params.yaml](params.yaml ':include :type=code yaml')

`launcher.yaml`

[launcher.yaml](launcher.yaml ':include :type=code yaml')


Run

```bash
fromconfig config.yaml params.yaml launcher.yaml - model - train
```

which prints

```
INFO:fromconfig_mlflow.launcher:Started run: http://127.0.0.1:5000/experiments/0/runs/<MLFLOW_RUN_ID>
INFO:fromconfig_mlflow.launcher:Logging artifacts config.json and launch.txt
INFO:fromconfig_mlflow.launcher:Logging parameters
Training model with learning_rate 0.001
```

If you navigate to `http://127.0.0.1:5000/experiments/0/runs/<MLFLOW_RUN_ID>` you should see your parameters and configs.

Note that we simply changed the `launcher.log` key to be a list of `logging, mlflow` to apply both loggers.

Of course, it also works with the command line overrides, for example

```
fromconfig config.yaml params.yaml --launcher.log=logging,mlflow --logging.level=20 - model - train
```


<a id="multi"></a>
## Advanced

Re-using the [quickstart](#quickstart) code, modify the `launcher.yaml` file

[launcher_advanced.yaml](launcher_advanced.yaml ':include :type=code yaml')

and run

```bash
fromconfig config.yaml params.yaml launcher_advanced.yaml - model - train
```

which prints

```
INFO:fromconfig_mlflow.launcher:Started run: http://127.0.0.1:5000/experiments/0/runs/<MLFLOW_RUN_ID>
INFO:fromconfig_mlflow.launcher:Logging artifacts config.json and launch_config.txt
INFO:fromconfig.launcher.parser:Resolved parser DefaultParser
INFO:fromconfig_mlflow.launcher:Active run found: http://127.0.0.1:5000/experiments/0/runs/<MLFLOW_RUN_ID>
INFO:fromconfig_mlflow.launcher:Logging artifacts parsed.json and launch_parsed.json
INFO:fromconfig_mlflow.launcher:Logging parameters
Training model with learning_rate 0.001
```

If you navigate to the MlFlow run, you should see
- the parameters, a flattened version of the *parsed* config (`model.learning_rate` is `0.001` and not `@params.learning_rate`)
- the original config, saved as `config.json`
- the parsed config, saved as `parsed.json`

Note that we run the logger in different steps, before parsing and after parsing. We also configure each launch of the `MlFlowLauncher` thanks to the `launches` entry.

<a id="options"></a>
## Options

To configure MlFlow, add a `mlflow` entry to your config.

You can set the following parameters

- `run_id`: if you wish to restart an existing run
- `run_name`: if you wish to give a name to your new run
- `tracking_uri`: to configure the tracking remote
- `experiment_name`: to use a different experiment than the custom experiment
- `artifact_location`: the location of the artifacts (config files)

Additionally, if you wish to call the `mlflow` launcher multiple times during the launch (for example once before the parser, and once after), you need to configure the different launches with the special `launches` key (otherwise only the first launch will actually log artifacts and parameters).

The `launches` key should be a list of dictionaries with the following parameters

- `log_artifacts`: if `True` (default), will log the artifacts (the config and command given to the launcher)
- `log_parameters`: if `True` (default) will log a flattened view of the parameters
- `path_config`: if given, will write the config as an artifact with that name (default is `config.json`)
- `path_command`: if given, will write the command as an artifact with that name (default is `launch.txt`, using the `.txt` extension because you can preview it on MlFlow).
- `include_keys`: if given, only log flattened parameters that have one of these keys as substring. Also shorten the flattened parameter to start at the first match. For example, if the config is `{"foo": {"bar": 1}}` and `include_keys=("bar",)`, then the logged parameter will be `"bar"`.
- `ignore_keys`: if given, parameters that have at least one of the keys as substring will be ignored.
