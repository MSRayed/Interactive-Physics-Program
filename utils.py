from enum import Enum

def pointInsideRect(x_min, y_min, x_max, y_max, px, py):
    return x_min <= px <= x_max and y_min <= py <= y_max

class Bound(Enum):
    LEFT = 1
    TOP = 2
    RIGHT = 3
    BOTTOM = 4

class ShapeType(Enum):
    CIRCLE = 1
    RECTANGLE = 2