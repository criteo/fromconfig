# Quickstart <!-- {docsify-ignore} -->

`fromconfig` can configure any Python object, without any change to the code.

As an example, let's consider a `model.py` module

[model.py](model.py ':include :type=code python')

with the following config files

`config.yaml`

[config.yaml](config.yaml ':include :type=code yaml')

`params.yaml`

[params.yaml](params.yaml ':include :type=code yaml')


## Command Line

In a terminal, run

```bash
fromconfig config.yaml params.yaml - model - train
```

which prints
```
Training model with learning_rate 0.1
```

The `fromconfig` command loads the config files, parse them, instantiate the result with `fromconfig.fromconfig` and then launch the `fire.Fire` command `- model - train` which roughly translate into "get the `model` key from the instantiated dictionary and execute the `train` method".

## Manual

You can also manipulate the configs manually.

[manual.py](manual.py ':include :type=code python')
