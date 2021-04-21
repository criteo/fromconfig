## Quickstart <!-- {docsify-ignore} -->

`fromconfig` can configure any Python object, without any change to the code.

As an example, let's consider a `foo.py` module

[foo.py](foo.py ':include :type=code python')


with the following config files


`config.yaml`

[config.yaml](config.yaml ':include :type=code yaml')

`params.yaml`

[params.yaml](params.yaml ':include :type=code yaml')


In a terminal, run

```bash
fromconfig config.yaml params.yaml - model - train
```

which prints
```
Training model with learning_rate 0.1
```

Here is a step-by-step breakdown of what is happening

1. Load the yaml files into dictionaries
2. Merge the dictionaries into a dictionary (`config`)
3. Instantiate the `DefaultLauncher` and call `launch(config, command)` where `command` is `model - train` ([Python Fire](https://github.com/google/python-fire) syntax).
4. The `DefaultLauncher` applies the `DefaultParser` to the `config` (it resolves references as `@params.learning_rate`, etc.)
5. Finally, the `DefaultLauncher` runs the `LocalLauncher`. It recursively instantiate sub-dictionaries, using the `_attr_` key to resolve the Python class / function as an import string. It then launches `fire.Fire(object, command)`, which translates into "get the `model` key from the instantiated dictionary and execute the `train` method".

This example can be found in [`examples/quickstart`](examples/quickstart).

To learn more about `FromConfig` features, see the [Usage Reference](usage-reference/config-syntax) and [Examples](examples/manual) sections.
