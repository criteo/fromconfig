# pylint: disable=unused-import,missing-docstring

from fromconfig.parser.base import Parser, Chain
from fromconfig.parser.evaluate import EvaluateParser
from fromconfig.parser.omega import OmegaConfParser
from fromconfig.parser.reference import ReferenceParser
from fromconfig.parser.singleton import SingletonParser


def DefaultParser() -> Parser:
    """Create default parser."""
    return Chain(OmegaConfParser(), ReferenceParser(), EvaluateParser(), SingletonParser())
