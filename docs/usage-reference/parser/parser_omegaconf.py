"""OmegaConfParser example."""

import fromconfig
import random


def random_hex() -> str:
    return hex(hash(random.random()))


if __name__ == "__main__":
    config = {
        "host": "localhost",
        "port": "8008",
        "url": "${host}:${port}",
        "path": "models/${now:}/${random_hex:}",  # Use  default resolver now + custom resolver
        "resolvers": {"random_hex": random_hex},  # Register custom resolver
    }
    parser = fromconfig.parser.OmegaConfParser()
    parsed = parser(config)
    print(parsed)
    assert parsed["url"] == "localhost:8008"
