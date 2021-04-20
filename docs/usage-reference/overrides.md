### Overrides <!-- {docsify-ignore} -->

You can provide additional key value parameters following the [Python Fire](https://github.com/google/python-fire) syntax as overrides directly via the command line.

For example

```bash
fromconfig config.yaml params.yaml --params.learning_rate=0.01 - model - train
```
will print

```
Training model with learning_rate 0.01
```

This is strictly equivalent to defining another config file (eg. `overrides.yaml`)

```yaml
params:
    learning_rate: 0.01
```

and running

```bash
fromconfig config.yaml params.yaml overrides.yaml - model - train
```

since the config files are merged from left to right, the files on the right overriding the existing keys from the left in case of conflict.
