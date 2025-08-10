from enum import Enum

def pointInsideRect(x_min, y_min, x_max, y_max, px, py):
    return x_min <= px <= x_max and y_min <= py <= y_max

class Bound(Enum):
    LEFT = 1
    TOP = 2
    RIGHT = 3
    BOTTOM = 4

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]