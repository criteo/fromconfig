# Hyper Params <!-- {docsify-ignore} -->


## Using the `HParamsLauncher`

By default, the [`DefaultLauncher`](usage-reference/launcher/) used by the CLI includes the `HParamsLauncher`, that launches multiple runs using the grid specified by the `hparams` entry.

Given the following module and config files (similar to the [quickstart](getting-started/quickstart/), we only changed `params` into `hparams`)

`model.py`

[model.py](model.py ':include :type=code python')

`config.yaml`

[config.yaml](config.yaml ':include :type=code yaml')

`hparams.yaml`

[hparams.yaml](hparams.yaml ':include :type=code yaml')

run

```bash
fromconfig config.yaml hparams.yaml - model - train
```

You should see plenty of logs and two trainings

```
========================[learning_rate=0.01]============================
Training model with learning_rate 0.01
========================[learning_rate=0.001]===========================
Training model with learning_rate 0.001
```

You can also specify the grid of hyper-parameter via CLI overrides.

For example,

```bash
fromconfig config.yaml --hparams.learning_rate=0.1,0.01 - model - train
```

## Manually

If you want to do something more custom, you can also easily manipulate the config manually.

For example,

[hp.py](hp.py ':include :type=code python')


## Custom Launcher

You can also [write your own `Launcher`](development/custom-launcher/) and [configure `fromconfig` to use your launcher](examples/configure-launcher/).
