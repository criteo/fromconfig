# Fire Config

## Fire Config

Imagine we have the following code

```python
class Model:
    """Dummy Model Class."""

    def __init__(self, learning_rate: float):
        self.learning_rate = learning_rate

    def forward(self, batch):
        print(f"Forward pass, batch = {batch}")

    def backward(self, batch):
        print(f"Backward pass, batch = {batch}, learning_rate = {self.learning_rate}")


def get_dataset(path: str):
    """Create Dataset from path."""
    # pylint: disable=unused-argument
    return [{"batch": 0}]


def train_model(model, dataset):
    """Train model on dataset."""
    for batch in dataset:
        model.forward(batch)
        model.backward(batch)
```

To train the model, we would do

```python
model = Model(0.1)
dataset = get_dataset("path/to/dataset")
train_model(model, dataset)
```

Now, let's say we want to provide a command line interface to train models.

The simplest way to do so is to define a `train_model` function with all the right arguments and use the python Fire library.

```python
import fire


def main(path_dataset: str, learning_rate: float):
    """Reload dataset, create model and train."""
    model = Model(learning_rate)
    dataset = get_dataset(path_dataset)
    train_model(model, dataset)


fire.Fire(main)
```

and then, we can do

```bash
python mylib.py --path_dataset=path --learning_rate=0.1
```

When the number of parameters and code complexity increase, this method does not scale.


Instead, we propose to scrap the `train_model` function entirely, and instead write a config file.

```bash
dataset:
  type: mylib.get_dataset
  path: path/to/dataset
model:
  type: mylib.Model
  learning_rate: 0.1
main:
  type: mylib.train_model
  model: "@model"
  dataset: "@dataset"
```

Not only does it provide a CLI, but it also allows you to organize the parameters, commit the actual run configuration, etc.

## Simple Pickle

One of the downsides of pickle is the lack of readability as well as size.

You can use `modelconfig` to configure the creation of objects, acting as a serialization format.

For example, our model can be serialized as follows

```bash
type: mylib.Model
learning_rate: 0.1
```

When your model needs to save its weights, you need to save and reload the weights separately

```python
import modelconfig


model.save_weights("path/to_weights")
model = modelconfig.from_config(config)
model.reload_weights("path/to/weights")
```


## Advanced

- immutable values (int, str, float, tuples)
- new instance of class
- singleton (dict, class, list, ...)
- raw config
- constructor of class @model()


config.yaml
yarn-config.yaml


deepr run config.yaml --yarn=yarn-config.yaml
----

deepr run pipeline.yaml model.yaml

```bash
# model1.yaml
model:
  type: Model1

# model2.yaml
model:
  type: Model2

# optimizer.yaml
optimizer:
  type: Optimizer

# train.yaml
train:
  type: Trainer
  model: None
  optimizer: @optimizer

# yarn1.yaml
local train = import train.yaml;
local model = import model.yaml;

main:
  train
  model:
```


```python
parsed = parse_config(config)  # Replace %
resolved = from_config(parsed)  # from_config


def train_on_yarn(yarn_config, trainer_config: Dict):
   job = resolved["job"]  # YarnTrainer(trainer=trainer_config)

```

```bash
model:
  type: Model
  eval: instance // call  # partial
  dim: 100
main:
  type: YarnTrainer
  model: @model
```

```bash
type: train_on_yarn
yarn_config:
  type: yarn_config
  num_cores: 48
trainer_config:
  eval: raw
  model:
    type: Model
    dim: 100
  main:
    type: YarnTrainer
    model: @model


######
local train = import train.yaml;

type: train_on_yarn
yarn_config:
  type: yarn_config
  num_cores: 48
trainer_config: train
```

Options:
1. jsonnet / yaml import inside config file to copy dict

Conclusion:
- Do not support dynamic config build (no `run model.json optimizer.json`) --> everything should be in imports in a final config file.


Jsonnet / Yaml
- import file (easy to do)
- local variables (jsonnet)
- modify variables (jsonnet)


```bash
# train.yaml
model:
  type: Model
  dim: 100
trainer:
  type: YarnTrainer
  model: @model
main:
  type: TrainOnYarn
  yarn_config:
    type: yarn_config
    num_cores: 48
  trainer_config:
    model: %model
    main: %trainer
```


```bash
# model.yaml
macro:
  eval: macro
  path: path/to/stuff/{date}

model:
  type: Model
  eval: singleton
  dim: 100

# pipeline.yaml
job:
  type: YarnTrainer
  config:
    path: @path
  trainer:
    eval: raw(path)
    model: @model
    main:
      type: Trainer
      model: @model
      path: @path
  # ---->
  #   model:
  #     type: Model
  #     dim: 100

  #   main:
  #     type: Trainer
  #     eval: None
  #     model: @model


```



# TODO
- cleanup specs and examples
- investigate "cleaner" ways of doing jsonnet stuff in yaml
- macro / call / partial / singleton
