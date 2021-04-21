"""Kwargs example."""

import fromconfig


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


if __name__ == "__main__":
    config = {"_attr_": "Point", "x": 0, "y": 1}
    point = fromconfig.fromconfig(config)
    assert isinstance(point, Point)
    assert point.x == 0
    assert point.y == 1
