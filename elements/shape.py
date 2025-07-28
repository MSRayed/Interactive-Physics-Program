from abc import ABC, abstractmethod

from tkinter import Canvas
from pymunk.vec2d import Vec2d

from utils import pointInsideRect


class Shape(ABC):
    def __init__(self):
        self._fill: str = "red"
        self._preview: bool = False
        self.p1: Vec2d = None
        self.p2: Vec2d = None

    def initiate(self, position):
        # **Assuming the point as top-left
        self.p1 = position

    def release(self, position):
        # Logic to check if the position is bottom-right or top-left
        self.p2 = position

    def if_valid(self):
        if self.p1 and self.p2:
            return Vec2d.get_distance(self.p1, self.p2) > 1
        return False
    
    def move(self, offset):
        self.p1 += offset
        self.p2 += offset
    
    @abstractmethod
    def draw(self, cnv: Canvas):
        pass

    def pointInside(self, point):
        px, py = point
        return pointInsideRect(self.left, self.top, self.right, self.bottom, px, py)

    @property
    def left(self): return min(self.p1.x, self.p2.x)
    @property
    def right(self): return max(self.p1.x, self.p2.x)
    @property
    def top(self): return min(self.p1.y, self.p2.y)
    @property
    def bottom(self): return max(self.p1.y, self.p2.y)

    @property
    def fill(self):
        return self._fill
    
    @fill.setter
    def fill(self, newFill):
        self._fill = newFill

    @property
    def preview(self):
        return self._preview
    
    @preview.setter
    def preview(self, newPreview):
        self._preview = newPreview


class Rectangle(Shape):
    def __init__(self):
        Shape.__init__(self)
        self.fill = "lightgreen"

    def draw(self, cnv):
        cnv.create_rectangle(self.p1.x, 
                            self.p1.y, 
                            self.p2.x, 
                            self.p2.y, 
                            fill=None if self.preview else self.fill)

class Oval(Shape):
    def __init__(self):
        Shape.__init__(self)
        self.fill = "red"

    def draw(self, cnv):
        cnv.create_oval(self.p1.x, 
                        self.p1.y, 
                        self.p2.x, 
                        self.p2.y, 
                        fill=None if self.preview else self.fill)