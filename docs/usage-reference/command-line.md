### Command Line <!-- {docsify-ignore} -->

Usage : call `fromconfig` on any number of paths to config files, with optional key value overrides. Use the full expressiveness of python Fire to manipulate the resulting instantiated object.

```bash
fromconfig config.yaml params.yaml --key=value - name
```

Supported formats : YAML, JSON, and [JSONNET](https://jsonnet.org).

The command line loads the different config files into Python dictionaries and merge them (if there is any key conflict, the config on the right overrides the ones from the left).

It then instantiate the `launcher` (using the `launcher` key if present in the config) and launches the config with the rest of the fire command.

With [Python Fire](https://github.com/google/python-fire), you can manipulate the resulting instantiated dictionary via the command line by using the fire syntax.

For example `fromconfig config.yaml - name` instantiates the dictionary defined in `config.yaml` and gets the value associated with the key `name`.
