# pylint: disable=unused-import,missing-docstring

from typing import Mapping

from fromconfig.parser.base import Parser
from fromconfig.parser.evaluate import EvaluateParser
from fromconfig.parser.omega import OmegaConfParser
from fromconfig.parser.reference import ReferenceParser
from fromconfig.parser.singleton import SingletonParser, singleton


class DefaultParser(Parser):
    """Default Parser.

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
        self.parsers = [OmegaConfParser(), ReferenceParser(), EvaluateParser(), SingletonParser()]

    def __call__(self, config: Mapping):
        parsed = config
        for parser in self.parsers:
            parsed = parser(parsed)
        return parsed
