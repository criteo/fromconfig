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

The `fromconfig` command loads the config files, parses them, instantiates the result with `fromconfig.fromconfig` and then launches the `fire.Fire` command `- model - train` which roughly translates into "get the `model` key from the instantiated dictionary and execute the `train` method".

__Warning__ It is not safe to use `fromconfig` with any config received from an untrusted source. Because it uses import strings to resolve attributes, it is as powerful as a plain python script and can execute arbitrary code.

## Manual

You can also manipulate the configs manually.

[manual.py](manual.py ':include :type=code python')
