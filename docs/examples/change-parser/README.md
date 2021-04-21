# Change Parser <!-- {docsify-ignore} -->

## Recommended Method

You can change the parser used by the `fromconfig` CLI.

For example, let's say we only want to apply the `SingletonParser` (instead of the `DefaultParser` that is applied by default).

Given the module and config

`model.py`

[model.py](model.py ':include :type=code python')

`config.yaml`

[config.yaml](config.yaml ':include :type=code yaml')

Create a new config file

`launcher.yaml`

[launcher.yaml](launcher.yaml ':include :type=code yaml')


and run

```bash
fromconfig config.yaml launcher.yaml - model - train
```

You should see

```
Training model with learning_rate @params.learning_rate
```

As expected, the `ReferenceParser` (part of the `DefaultParser` and responsible for resolving the `@params.learning_rate` reference) is not applied, and instead, only the `SingletonParser` is applied.


## Custom Launcher

If you use a custom launcher, note that you may be disabling parsing as it is merely one of the steps executed by the `DefaultLauncher`. The `ParserLauncher` part of the `DefaultLauncher` instantiates the `parser` from the config's `parser` key and applies parsing during launch.

As long as the `ParserLauncher` is ran by your custom `Launcher`, the recommended method should work.

You can also [write your own `Launcher`](development/custom-launcher/) that will be responsible for parsing and [configure `fromconfig` to use your launcher](examples/configure-launcher/).
