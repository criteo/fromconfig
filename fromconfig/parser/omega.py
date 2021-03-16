"""Simple OmegaConf parser."""

from typing import Mapping

from omegaconf import OmegaConf

from fromconfig.parser import base


class OmegaConfParser(base.Parser):
    """Simple OmegaConf parser.

    Example
    -------
    >>> import fromconfig
    >>> config = {
    ...     "host": "localhost",
    ...     "port": "8008",
    ...     "url": "${host}:${port}"
    ... }
    >>> parser = fromconfig.parser.OmegaConfParser()
    >>> parsed = parser(config)
    >>> parsed["url"]
    'localhost:8008'
    """

    def __call__(self, config: Mapping) -> Mapping:
        conf = OmegaConf.create(config)  # type: ignore
        return OmegaConf.to_container(conf, resolve=True)  # type: ignore
