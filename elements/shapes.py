from abc import ABC, abstractmethod

from tkinter import Canvas
from pymunk.vec2d import Vec2d


class Shape(ABC):
    def __init__(self):
        self._fill: str = "red"
        self._preview: bool = False

    @abstractmethod
    def initiate(self, position: Vec2d):
        pass

    @abstractmethod
    def release(self, position: Vec2d):
        pass
    
    @abstractmethod
    def draw(self, cnv: Canvas):
        pass

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
        self.topleft: Vec2d = None
        self.bottomright: Vec2d = None

    def initiate(self, position):
        self.topleft = position
    
    def release(self, position):
        self.bottomright = position

    def draw(self, cnv):
        return cnv.create_rectangle(self.topleft.x, 
                                    self.topleft.y, 
                                    self.bottomright.x, 
                                    self.bottomright.y, 
                                    fill=self.fill, 
                                    stipple="gray50" if self.preview else None)


class Oval(Shape):
    def __init__(self):
        Shape.__init__(self)
        self.fill = "red"
        self.topleft: Vec2d = None
        self.bottomright: Vec2d = None

    def initiate(self, position):
        self.topleft = position
    
    def release(self, position):
        self.bottomright = position

    def draw(self, cnv):
        return cnv.create_oval(self.topleft.x, 
                               self.topleft.y, 
                               self.bottomright.x, 
                               self.bottomright.y, 
                               fill=self.fill, 
                               stipple="gray50" if self.preview else None)