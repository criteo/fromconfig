"""ReferenceParser simple example."""

import fromconfig


if __name__ == "__main__":
    parser = fromconfig.parser.ReferenceParser()
    config = {"params": {"x": 1}, "y": "@params.x"}
    parsed = parser(config)
    assert parsed["y"] == 1
