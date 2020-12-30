"""Macro Parser."""

import logging
from typing import Mapping

from fromconfig.core import fromconfig
from fromconfig.parser import base
from fromconfig.parser.reference import ReferenceParser


LOGGER = logging.getLogger(__name__)


class MacroParser(base.Parser):
    """Macro Parser.

    Example
    -------
    >>> import fromconfig
    >>> parser = fromconfig.parser.MacroParser()
    >>> config = {"_macro_": {"x": 1}, "_config_": {"y": "@x"}}
    >>> parsed = parser(config)
    >>> parsed["x"]
    1

    Attributes
    ----------
    allow_override : bool, default = True
        If True, allow macros to override keys from config.
    """

    MACRO = "_macro_"
    CONFIG = "_config_"

    def __call__(self, config: Mapping):
        # If no macro or config key, return unchanged
        if self.MACRO not in config and self.CONFIG not in config:
            LOGGER.info(f"No {self.MACRO} or {self.CONFIG} key found in config.")
            return config

        # Check that there is no unexpected keys
        if any(key not in (self.MACRO, self.CONFIG) for key in config):
            raise ValueError(f"Unexpected keys in config {config} (expected {self.MACRO} and {self.CONFIG})")

        # Extract sub config
        subconfig = config.get(self.CONFIG)
        if subconfig is None:
            LOGGER.warning(f"No config found (missing {self.CONFIG} key in {config})")
            return {}

        # Resolve macro
        macro = fromconfig(config.get(self.MACRO, {}))
        if not isinstance(macro, Mapping):
            raise TypeError(f"Expected type Mapping but got {type(macro)}")

        # Replace macro references
        parser = ReferenceParser(keys=list(macro), allow_missing=False)
        return parser({self.CONFIG: subconfig, **macro})[self.CONFIG]
