"""Evaluate parser."""

import logging
from typing import Mapping

from fromconfig import Keys
from fromconfig.utils import StrEnum, depth_map, is_mapping
from fromconfig.parsers.base import Parser


LOGGER = logging.getLogger(__name__)


class EvaluateMode(StrEnum):
    """Evaluation modes."""

    CALL = "call"
    PARTIAL = "partial"
    IMPORT = "import"


class EvaluateParser(Parser):
    """Evaluate parser."""

    KEY = "_eval_"

    def __call__(self, config: Mapping):
        """Parses configs with _eval_ key into valid config."""

        def _map_fn(item):
            if is_mapping(item) and self.KEY in item:
                # Get mode, attribute name, args, and kwargs from item
                evaluate = EvaluateMode(item[self.KEY])
                name = item.get(Keys.ATTR)
                args = item.get(Keys.ARGS, [])
                kwargs = {key: value for key, value in item.items() if key not in (self.KEY, Keys.ATTR, Keys.ARGS)}

                # If IMPORT, should just import the attribute
                if evaluate == EvaluateMode.IMPORT:
                    if args or kwargs:
                        msg = f"Found {args} {kwargs} in item {item}, expected only {Keys.ATTR} (evaluate = {evaluate})"
                        raise ValueError(msg)
                    if name is None:
                        raise ValueError(f"No {Keys.ATTR} found in item {item} (evaluate = {evaluate})")
                    return {Keys.ATTR: "fromconfig.utils.import_from_string", Keys.ARGS: name}

                # If PARTIAL, wrap type (if present)
                if evaluate == EvaluateMode.PARTIAL:
                    if name is None:
                        raise ValueError(f"No {Keys.ATTR} found in item {item} (evaluate = {evaluate})")
                    fn = {Keys.ATTR: "fromconfig.utils.import_from_string", Keys.ARGS: name}
                    return {Keys.ATTR: "functools.partial", Keys.ARGS: [fn, *args], **kwargs}

                # If CALL, nothing to do (default behavior)
                if evaluate == EvaluateMode.CALL:
                    return {Keys.ATTR: name, Keys.ARGS: args, **kwargs}

            return item

        return depth_map(_map_fn, config)
