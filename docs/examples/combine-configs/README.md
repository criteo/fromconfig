# Combine Configs <!-- {docsify-ignore} -->

## Dynamically

As shown in the [Machine Learning] example, it is practical in many scenarios to be able to combine different config files dynamically.

Given a module `ml.py` defining model, optimizer and trainer classes

[ml.py](ml.py ':include :type=code python')

And the following config files

`trainer.yaml`

[trainer.yaml](trainer.yaml ':include :type=code yaml')

`model.yaml`

[model.yaml](model.yaml ':include :type=code yaml')

`optimizer.yaml`

[optimizer.yaml](optimizer.yaml ':include :type=code yaml')

`params/big.yaml`

[params/big.yaml](params/big.yaml ':include :type=code yaml')

`params/small.yaml`

[params/small.yaml](params/small.yaml ':include :type=code yaml')


It is possible to launch two different trainings with different set of hyper-parameters with

```bash
fromconfig trainer.yaml model.yaml optimizer.yaml params/small.yaml - trainer - run
fromconfig trainer.yaml model.yaml optimizer.yaml params/big.yaml - trainer - run
```

which should print

```
Training Model(dim=10) with Optimizer(learning_rate=0.01)
Training Model(dim=100) with Optimizer(learning_rate=0.001)
```

## Organize and Include

One caveat of being able to split your configuration across different files is that the command line starts to grow in size, deserving the purpose of simplicity.

Of course, we could try to maintain at most one config file for the things that are not supposed to change, and another set of files that represent variations of the global configuration. However, it would be to the detriment of readability, since having self-contained and short config files configuring one component is a huge advantage.

To get the best of both worlds, `fromconfig.load` supports a [special YAML `Loader` that enables includes](https://stackoverflow.com/questions/528281/how-can-i-include-a-yaml-file-inside-another). Similar to JSONNET (and its [import mechanism](https://jsonnet.org/learning/tutorial.html)), it is possible to statically include a YAML file into another.

For example,

`config.yaml`

[config.yaml](config.yaml ':include :type=code yaml')
