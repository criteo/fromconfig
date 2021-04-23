# Machine Learning <!-- {docsify-ignore} -->

`fromconfig` is particularly well suited for Machine Learning as it is common to have a lot of different parameters, sometimes far down the call stack, and different configurations of these hyper-parameters.

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
Saving Model(dim=10) to models/2021-04-23-12-05-47
Training Model(dim=100) with Optimizer(learning_rate=0.001)
Saving Model(dim=100) to models/2021-04-23-12-05-48
```

We used the custom resolver `now` with the `OmegaConfParser` to generate a path for the model (see `"models/${now:}"`). Read more about the interpolation mechanism (you can register your own resolvers) in the [Usage Reference](usage-reference/parser/).

Note that it is encouraged to save these config files with the experiment's files to get full reproducibility. [MlFlow](https://mlflow.org) is an open-source platform that tracks your experiments by logging metrics and artifacts.
