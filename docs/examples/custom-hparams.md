### Custom Hyper-Parameter Search <!-- {docsify-ignore} -->

You can use the `hparams` entry, that the `HParamsLauncher` uses to generate configs (see [launcher](usage-reference/launcher)).

Reusing the [ML example](examples/machine-learning), simply add a `hparams.yaml` file

```yaml
params:
  dim: "@hparams.dim"
  learning_rate: "@hparams.learning_rate"

hparams:
  dim: [10, 100]
  learning_rate: [0.1, 0.01]
```

And launch a hyper-parameter sweep with

```bash
fromconfig trainer.yaml model.yaml optimizer.yaml hparams.yaml - trainer - run
```

which should print

```
Training Model(dim=10) with Optimizer(learning_rate=0.1)
Training Model(dim=10) with Optimizer(learning_rate=0.01)
Training Model(dim=100) with Optimizer(learning_rate=0.1)
Training Model(dim=100) with Optimizer(learning_rate=0.01)
```

You can also write your custom config generator (and even make it a `Launcher`, see [how to implement a custom Launcher](examples/custom-launcher)).

For example, something that is equivalent to what we just did is

```python
import fromconfig


if __name__ == "__main__":
    config = {
        "model": {
            "_attr_": "ml.Model",
            "dim": "@params.dim"
        },
        "optimizer": {
            "_attr_": "ml.Optimizer",
            "learning_rate": "@params.learning_rate"
        },
        "trainer": {
            "_attr_": "ml.Trainer",
            "model": "@model",
            "optimizer": "@optimizer"
        }
    }
    parser = fromconfig.parser.DefaultParser()
    for dim in [10, 100]:
        for learning_rate in [0.01, 0.1]:
            params = {
                "dim": dim,
                "learning_rate": learning_rate
            }
            parsed = parser({**config, "params": params})
            trainer = fromconfig.fromconfig(parsed)["trainer"]
            trainer.run()
            # Clear the singletons if any as we most likely don't want
            # to share between configs
            fromconfig.parser.singleton.clear()
```

which prints

```
Training Model(dim=10) with Optimizer(learning_rate=0.01)
Training Model(dim=10) with Optimizer(learning_rate=0.1)
Training Model(dim=100) with Optimizer(learning_rate=0.01)
Training Model(dim=100) with Optimizer(learning_rate=0.1)
```

This example can be found in [`examples/ml`](examples/ml) (run `python hp.py`).
