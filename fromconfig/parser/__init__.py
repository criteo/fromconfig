# pylint: disable=unused-import,missing-docstring

from fromconfig.parser.base import Parser, ChainParser
from fromconfig.parser.evaluate import EvaluateParser
from fromconfig.parser.default import DefaultParser
from fromconfig.parser.omega import OmegaConfParser
from fromconfig.parser.reference import ReferenceParser
from fromconfig.parser.singleton import SingletonParser, singleton


class CustomParser(Parser):
    def __call__(self, config):
        run_name = "learning_rate_" + str(config["params"]["learning_rate"])
        return DefaultParser()({**config, **{"mlflow": {"run_name": run_name}}})
