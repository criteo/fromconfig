"""Macro Parser."""

import logging
from typing import Mapping

from fromconfig.core import fromconfig
from fromconfig.utils import merge_dict
from fromconfig.parser import base


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

    def __init__(self, allow_override: bool = True):
        self.allow_override = allow_override

    def __call__(self, config: Mapping):
        # If no macro or config key, return unchanged
        if self.MACRO not in config and self.CONFIG not in config:
            LOGGER.info(f"No {self.MACRO} or {self.CONFIG} key found in config.")

        # Check that there is no unexpected keys
        if any(key not in (self.MACRO, self.CONFIG) for key in config):
            raise ValueError(f"Unexpected keys in config {config} (expected {self.MACRO} and {self.CONFIG})")

        # Resolve macro
        macro = fromconfig(config.get(self.MACRO, {}))
        if not isinstance(macro, Mapping):
            raise TypeError(f"Expected type Mapping but got {type(macro)}")

        # Merge macro and config entry
        return merge_dict(config.get(self.CONFIG, {}), macro, allow_override=self.allow_override)
