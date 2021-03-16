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
    >>> config = {
    ...     "model": {
    ...         "_attr_": "mylib.models.MyModel",
    ...         "_singleton_": "my_model",
    ...         "model_dir": "${data.root}/${data.model}"
    ...     },
    ...     "data": {
    ...         "root": "/path/to/root",
    ...         "model": "subdir/for/model"
    ...     },
    ...     "trainer": {
    ...         "_attr_": "mylib.train.Trainer",
    ...         "model": "@model",
    ...     }
    ... }
    >>> parser = fromconfig.parser.DefaultParser()
    >>> parsed = parser(config)
    >>> sorted(parsed["model"])  # Now wrapped into singleton
    ['_attr_', 'constructor', 'key']
    >>> parsed["model"] == parsed["trainer"]["model"]  # Reference
    True
    >>> parsed["model"]["constructor"]["model_dir"]  # Interpolation
    '/path/to/root/subdir/for/model'
    """

    def __init__(self):
        self.parsers = [OmegaConfParser(), ReferenceParser(), EvaluateParser(), SingletonParser()]

    def __call__(self, config: Mapping):
        parsed = config
        for parser in self.parsers:
            parsed = parser(parsed)
        return parsed
