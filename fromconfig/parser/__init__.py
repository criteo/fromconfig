# pylint: disable=unused-import,missing-docstring

from typing import Callable

from fromconfig.parser.base import Parser, Chain, Select
from fromconfig.parser.evaluate import EvaluateMode, EvaluateParser
from fromconfig.parser.macro import MacroParser
from fromconfig.parser.reference import ReferenceParser
from fromconfig.parser.rename import RenameParser
from fromconfig.parser.singleton import SingletonParser


_STANDARD = Chain(ReferenceParser(), EvaluateParser(), SingletonParser())

_DEFAULT = Chain(Select(key=MacroParser.MACRO, parser=_STANDARD), MacroParser(), _STANDARD)


def parse(config, parser: Callable = _DEFAULT):
    return parser(config) if parser else config
