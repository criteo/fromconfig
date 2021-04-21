## Cheat Sheet <!-- {docsify-ignore} -->


### Syntax and default options

`fromconfig.fromconfig` special keys


| Key        | Value Example       | Use                                               |
|------------|---------------------|---------------------------------------------------|
| `"_attr_"` | `"foo.bar.MyClass"` | Full import string of a class, function or method |
| `"_args_"` | `[1, 2]`            | Positional arguments                              |

`fromconfig.parser.DefaultParser` syntax

| Key             | Value                             | Use                                    |
|-----------------|-----------------------------------|----------------------------------------|
| `"_singleton_"` | `"my_singleton_name"`             | Creates a singleton identified by name |
| `"_eval_"`      | `"call"`, `"import"`, `"partial"` | Evaluation modes                       |
|                 | `"@params.model"`                 | Reference                              |
|                 | `"${params.url}:${params.port}"`  | Interpolation via OmegaConf            |

`fromconfig.parser.DefaultLauncher` options (keys at config's toplevel)


| Key         | Value Example                                      | Use                                         |
|-------------|----------------------------------------------------|---------------------------------------------|
| `"logging"` | `{"level": 20}`                                    | Change logging level to 20 (`logging.INFO`) |
| `"parser"`  | `{"_attr_": "fromconfig.parser.DefaultParser"}`    | Configure which parser is used              |
| `"hparams"` | `{"learning_rate": [0.1, 0.001]}`                  | Hyper-parameter search (use references like `@hparams.learning_rate` in other parts of the config)             |


### Config sample

As an example, let's consider a `foo.py` module

[foo.py](foo.py ':include :type=code python')

with the following config file

`config.yaml`

[config.yaml](config.yaml ':include :type=code yaml')

In a terminal, run

```bash
fromconfig config.yaml - model - train
```
