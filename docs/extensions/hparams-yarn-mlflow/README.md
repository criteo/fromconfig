# HParams + Yarn + MlFlow <!-- {docsify-ignore} -->

<a id="install"></a>
## Install

```bash
pip install fromconfig_yarn fromconfig_mlflow
```

## Quickstart

To activate both yarn and MlFlow, simply add `--launcher.log=mlflow --launcher.run=yarn,mlflow,local` to your command.

```bash
fromconfig config.yaml hparams.yaml --launcher.log=mlflow --launcher.run=yarn,mlflow,local - model - train
```

Simply specifying `--launcher.run=yarn` would not be sufficient. Adding `mlflow,local` restarts the MlFlow run on the distant machine, thanks to the MlFlow environment variables that are automatically set and forwarded by default.

With

`model.py`

[model.py](model.py ':include :type=code python')

`config.yaml`

[config.yaml](config.yaml ':include :type=code yaml')

`hparams.yaml`

[hparams.yaml](hparams.yaml ':include :type=code yaml')

It should print

```
============================================[learning_rate=0.1]============================================
Started run: http://127.0.0.1:5000/experiments/0/runs/1c8b62d08d134cdda4e0ac545e8a804c
Uploading PEX and running on YARN
Active run found: http://127.0.0.1:5000/experiments/0/runs/1c8b62d08d134cdda4e0ac545e8a804c
Training model with learning_rate 0.1
===========================================[learning_rate=0.01]===========================================
Started run: http://127.0.0.1:5000/experiments/0/runs/3a78d8c011884e2fb8d4b2813cf398dc
Uploading PEX and running on YARN
Active run found: http://127.0.0.1:5000/experiments/0/runs/3a78d8c011884e2fb8d4b2813cf398dc
Training model with learning_rate 0.01
```

You can also monkeypatch the relevant functions to "fake" the Hadoop environment with

```bash
python monkeypatch_fromconfig.py config.yaml hparams.yaml --launcher.log=mlflow --launcher.run=yarn,mlflow,local - model - train
```

You can also use a `launcher.yaml` file

[launcher.yaml](launcher.yaml ':include :type=code yaml')

And launch with

```bash
fromconfig config.yaml hparams.yaml launcher.yaml - model - train
```


## Advanced

You can configure each launcher more precisely. See the [mlflow](/extensions/mlflow/) and [yarn](/extensions/yarn/) references.

For example,

[launcher_advanced.yaml](launcher_advanced.yaml ':include :type=code yaml')

