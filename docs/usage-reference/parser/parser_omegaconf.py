"""OmegaConfParser example."""

import fromconfig


if __name__ == "__main__":
    config = {"host": "localhost", "port": "8008", "url": "${host}:${port}"}
    parser = fromconfig.parser.OmegaConfParser()
    parsed = parser(config)
    assert parsed["url"] == "localhost:8008"
