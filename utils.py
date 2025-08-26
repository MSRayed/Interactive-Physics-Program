from enum import Enum
from math import cos, sin, sqrt

from pymunk import Vec2d

def point_inside_circle(px, py, cx, cy, r):
    distance = sqrt((px - cx)**2 + (py - cy)**2)
    return distance <= r

def point_inside_rect(x_min, y_min, x_max, y_max, px, py):
    return x_min <= px <= x_max and y_min <= py <= y_max

def polar_to_cartesian(polar_tuple):
    """Convert polar coordinates (angle, radius) to Cartesian coordinates."""
    radius, angle = polar_tuple
    return Vec2d(radius * cos(angle), radius * sin(angle))

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