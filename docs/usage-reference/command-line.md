# Command Line <!-- {docsify-ignore} -->

## Usage

Usage : call `fromconfig` on any number of paths to config files, with optional key value overrides. Use the full expressiveness of [python Fire](https://github.com/google/python-fire) to manipulate the resulting instantiated object.

```bash
fromconfig config.yaml params.yaml --key=value - name
```

Supported formats : YAML, JSON, and [JSONNET](https://jsonnet.org).

The command line loads the different config files into Python dictionaries and merge them (if there is any key conflict, the config on the right overrides the ones from the left).

It then instantiate the [`launcher`](usage-reference/launcher/) (using the `launcher` key if present in the config) and launches the config with the rest of the fire command. The `launcher` is responsible for parsing (resolving interpolation, etc.), and uses a [`Parser`](usage-reference/parser/).

With [Python Fire](https://github.com/google/python-fire), you can manipulate the resulting instantiated dictionary via the command line by using the fire syntax.

For example `fromconfig config.yaml - name` instantiates the dictionary defined in `config.yaml` and gets the value associated with the key `name`.


## Overrides <!-- {docsify-ignore} -->

You can provide additional key value parameters following the [Python Fire](https://github.com/google/python-fire) syntax as overrides directly via the command line.

For example, using the [quickstart](getting-started/quickstart)'s material, running

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
