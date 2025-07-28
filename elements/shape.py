from abc import ABC, abstractmethod

from tkinter import Canvas
from pymunk.vec2d import Vec2d


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
    
    @abstractmethod
    def draw(self, cnv: Canvas):
        pass

    def pointInside(self, point):
        px, py = point
        x_min = min(self.p1.x, self.p2.x)
        x_max = max(self.p1.x, self.p2.x)
        y_min = min(self.p1.y, self.p2.y)
        y_max = max(self.p1.y, self.p2.y)

        return x_min <= px <= x_max and y_min <= py <= y_max

    def get_left_boundary(self): return min(self.p1.x, self.p2.x)
    def get_right_boundary(self): return max(self.p1.x, self.p2.x)
    def get_top_boundary(self): return min(self.p1.y, self.p2.y)
    def get_bottom_boundary(self): return max(self.p1.y, self.p2.y)

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
        return cnv.create_rectangle(self.p1.x, 
                                    self.p1.y, 
                                    self.p2.x, 
                                    self.p2.y, 
                                    fill=None if self.preview else self.fill)


class Oval(Shape):
    def __init__(self):
        Shape.__init__(self)
        self.fill = "red"

    def draw(self, cnv):
        return cnv.create_oval(self.p1.x, 
                                    self.p1.y, 
                                    self.p2.x, 
                                    self.p2.y, 
                                    fill=None if self.preview else self.fill)