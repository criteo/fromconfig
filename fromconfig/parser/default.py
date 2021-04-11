"""Default Parser."""

from fromconfig.parser import base
from fromconfig.parser.omega import OmegaConfParser
from fromconfig.parser.reference import ReferenceParser
from fromconfig.parser.evaluate import EvaluateParser
from fromconfig.parser.singleton import SingletonParser


class DefaultParser(base.ChainParser):
    """Create Default Parser.

    Example
    -------
    >>> import fromconfig
    >>> class Model:
    ...     def __init__(self, model_dir):
    ...         self.model_dir = model_dir
    >>> class Trainer:
    ...     def __init__(self, model):
    ...         self.model = model
    >>> config = {
    ...     "model": {
    ...         "_attr_": "Model",
    ...         "_singleton_": "my_model",
    ...         "model_dir": "${data.root}/${data.model}"
    ...     },
    ...     "data": {
    ...         "root": "/path/to/root",
    ...         "model": "subdir/for/model"
    ...     },
    ...     "trainer": {
    ...         "_attr_": "Trainer",
    ...         "model": "@model",
    ...     }
    ... }
    >>> parser = fromconfig.parser.DefaultParser()
    >>> parsed = parser(config)
    >>> instance = fromconfig.fromconfig(parsed)
    >>> id(instance["model"]) == id(instance["trainer"].model)
    True
    >>> instance["model"].model_dir == "/path/to/root/subdir/for/model"
    True
    """

    def __init__(self):
        super().__init__(OmegaConfParser(), ReferenceParser(), EvaluateParser(), SingletonParser())
