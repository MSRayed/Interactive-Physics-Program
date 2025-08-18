import math

from enum import Enum

def point_inside_rect(x_min, y_min, x_max, y_max, px, py):
    return x_min <= px <= x_max and y_min <= py <= y_max

def point_in_circle(px, py, cx, cy, r):
    distance = math.sqrt((px - cx)**2 + (py - cy)**2)
    return distance <= r

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