"""Evaluate parser."""

import logging
from typing import Mapping

from fromconfig.core import Keys
from fromconfig.parser import base
from fromconfig.utils import StrEnum, depth_map, is_mapping


LOGGER = logging.getLogger(__name__)


class EvaluateMode(StrEnum):
    """Evaluation modes."""

    CALL = "call"
    PARTIAL = "partial"
    IMPORT = "import"


class EvaluateParser(base.Parser):
    """Evaluate parser."""

    KEY = "_eval_"

    def __call__(self, config: Mapping):
        """Parses configs with _eval_ key into valid config."""

        def _map_fn(item):
            if is_mapping(item) and self.KEY in item:
                # Get mode, attribute name, args, and kwargs from item
                evaluate = EvaluateMode(item[self.KEY])
                name = item[Keys.ATTR]
                args = item.get(Keys.ARGS, [])
                kwargs = {key: value for key, value in item.items() if key not in (self.KEY, Keys.ATTR, Keys.ARGS)}

                # If IMPORT, should just import the attribute
                if evaluate == EvaluateMode.IMPORT:
                    if args or kwargs:
                        msg = f"Found {args} {kwargs} in item {item}, expected only {Keys.ATTR} (evaluate = {evaluate})"
                        raise ValueError(msg)
                    return {Keys.ATTR: "fromconfig.utils.import_from_string", Keys.ARGS: [name]}

                # If PARTIAL, wrap type (if present)
                if evaluate == EvaluateMode.PARTIAL:
                    fn = {Keys.ATTR: "fromconfig.utils.import_from_string", "name": name}
                    return {Keys.ATTR: "functools.partial", Keys.ARGS: [fn, *args], **kwargs}

                # If CALL, nothing to do (default behavior)
                if evaluate == EvaluateMode.CALL:
                    return {Keys.ATTR: name, Keys.ARGS: args, **kwargs}

            return item

        return depth_map(_map_fn, config)
