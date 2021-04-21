"""ReferenceParser full example."""

import fromconfig


if __name__ == "__main__":
    param1 = {"params": {"x": 1}}
    param2 = {"params": {"x": 2}}
    config = {"model": {"x": "@params.x"}}
    parser = fromconfig.parser.ReferenceParser()
    parsed1 = parser({**config, **param1})
    assert parsed1["model"]["x"] == 1
    parsed2 = parser({**config, **param2})
    assert parsed1["model"]["x"] == 2
