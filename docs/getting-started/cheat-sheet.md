## Cheat Sheet <!-- {docsify-ignore} -->


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


Config sample

```yaml
# Configure model
model:
  _attr_: foo.Model  # Full import string to the class to instantiate
  _args_: ["@hparams.dim"]  # Positional arguments
  _singleton_: "model_${hparams.dim}_${hparams.learning_rate}"  # All @model references will instantiate the same object with that name
  _eval_: "call"  # Optional ("call" is the default behavior)
  learning_rate: "@hparams.learning_rate"  # Other key value parameter

# Configure hyper parameters, use references @hparams.key to use them
hparams:
  learning_rate: [0.1, 0.001]
  dim: [10, 100]

# Configure logging level (set to logging.INFO)
logging:
  level: 20

# Configure parser (optional, using this parser is the default behavior)
parser:
  _attr_: "fromconfig.parser.DefaultParser"

# Configure launcher (optional, the following config creates the same launcher as the default behavior)
launcher:
  sweep: "hparams"
  parse: "parser"
  log: "logging"
  run: "local"

```

for module

```python
class Model:
    def __init__(self, dim: int, learning_rate: float):
        self.dim = dim
        self.learning_rate = learning_rate

    def train(self):
        print(f"Training model({self.dim}) with learning_rate {self.learning_rate}")
```

Launch with

```bash
fromconfig config.yaml - model - train
```

This example can be found in [`examples/cheat_sheet`](examples/cheat_sheet).
