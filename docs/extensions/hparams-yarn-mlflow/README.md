# FromConfig HParams + Yarn + MlFlow <!-- {docsify-ignore} -->


<a id="install"></a>
## Install

```bash
pip install fromconfig_yarn fromconfig_mlflow
```

## Quickstart

Given the following module

[model.py](model.py ':include :type=code python')

and config files

`config.yaml`

[config.yaml](config.yaml ':include :type=code yaml')

`hparams.yaml`

[hparams.yaml](hparams.yaml ':include :type=code yaml')

`launcher.yaml`

[launcher.yaml](launcher.yaml ':include :type=code yaml')

Run (assuming you are in a Hadoop environment)

```bash
fromconfig config.yaml hparams.yaml launcher.yaml - model - train
```

You can also monkeypatch the relevant functions to "fake" the Hadoop environment with

```bash
python monkeypatch_fromconfig.py config.yaml hparams.yaml launcher.yaml - model - train
```

which should print

```
INFO:fromconfig_mlflow.launcher:Started run
INFO:fromconfig_mlflow.launcher:Logging artifacts config.json and launch_config.txt
INFO:fromconfig_mlflow.launcher:Logging artifacts parsed.json and launch_parsed.json
INFO:fromconfig_mlflow.launcher:Logging parameters
INFO:fromconfig_yarn.launcher:Uploading pex
Monkey Training on Yarn
Training model with learning_rate 0.1
INFO:fromconfig_mlflow.launcher:Started run
INFO:fromconfig_mlflow.launcher:Logging artifacts config.json and launch_config.txt
INFO:fromconfig_mlflow.launcher:Logging artifacts parsed.json and launch_parsed.json
INFO:fromconfig_mlflow.launcher:Logging parameters
INFO:fromconfig_yarn.launcher:Uploading pex
Training model with learning_rate 0.01
```
