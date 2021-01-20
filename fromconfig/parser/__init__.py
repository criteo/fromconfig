# pylint: disable=unused-import,missing-docstring

from typing import Callable

from fromconfig.parser.base import Parser, Chain
from fromconfig.parser.evaluate import EvaluateMode, EvaluateParser
from fromconfig.parser.reference import ReferenceParser, is_reference, reference_to_keys
from fromconfig.parser.rename import RenameParser
from fromconfig.parser.singleton import SingletonParser


DEFAULT = Chain(ReferenceParser(), EvaluateParser(), SingletonParser())


def parse(config, parser: Callable = DEFAULT):
    return parser(config) if parser else config
