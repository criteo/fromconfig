import fromconfig


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


config = {"_attr_": "Point", "x": 0, "y": 0}
fromconfig.fromconfig(config)  # Point(0, 0)
