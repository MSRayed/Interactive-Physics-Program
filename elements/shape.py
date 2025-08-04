from abc import ABC, abstractmethod

from tkinter import Canvas

from utils import pointInsideRect, Bound


class Shape(ABC):
    NAME: str = "shape"
    
    def __init__(self):
        self.fill: str = "red"
        self.preview: bool = False
        
        self.left: float = None
        self.right: float = None
        self.top: float = None
        self.bottom: float = None
    
    def resize(self, boundX: Bound, boundY: Bound, newX, newY):
        if boundX == Bound.LEFT:
            self.left = newX
        if boundX == Bound.RIGHT:
            self.right = newX
        if boundY == Bound.TOP:
            self.top = newY
        if boundY == Bound.BOTTOM:
            self.bottom = newY

    def if_valid(self):
        return self.left != self.right and self.top != self.bottom
    
    @abstractmethod
    def draw(self, cnv: Canvas):
        pass

    def pointInside(self, point):
        px, py = point
        return pointInsideRect(self.left, self.top, self.right, self.bottom, px, py)
    
    def fixOrientation(self):
        # If the sides are opposite
        if self.left > self.right:
            self.left, self.right = self.right, self.left
        if self.top > self.bottom:
            self.bottom, self.top = self.top, self.bottom