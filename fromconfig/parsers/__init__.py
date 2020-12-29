# pylint: disable=unused-import,missing-docstring

from typing import Callable

from fromconfig.parsers.base import Parser, Chain, Select
from fromconfig.parsers.evaluate import EvaluateMode, EvaluateParser
from fromconfig.parsers.macro import MacroParser
from fromconfig.parsers.reference import ReferenceParser
from fromconfig.parsers.rename import RenameParser
from fromconfig.parsers.singleton import SingletonParser


_STANDARD = Chain(ReferenceParser(), EvaluateParser(), SingletonParser())

_DEFAULT = Chain(Select(key=MacroParser.MACRO, parser=_STANDARD), MacroParser(), _STANDARD)


def parse(config, parser: Callable = _DEFAULT):
    return parser(config) if parser else config
