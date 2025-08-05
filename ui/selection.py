from tkinter import Canvas
from pymunk.vec2d import Vec2d

from elements import Shape
from utils import pointInsideRect, Bound


class Selection:
    def __init__(self, cnv: Canvas):
        self.cnv = cnv
        self.padding = 3
        self.curr = None
        self.lastCorner = None
    
    def getMouseOnCorner(self, mouse: Vec2d):
        if not self.curr:
            return None
        
        for (x, boundX) in zip([self.curr.left, self.curr.right], [Bound.LEFT, Bound.RIGHT]):
            for (y, boundY) in zip([self.curr.top, self.curr.bottom], [Bound.TOP, Bound.BOTTOM]):
                if pointInsideRect(x-self.padding, y-self.padding, x+self.padding, y+self.padding, mouse.x, mouse.y):
                    self.lastCorner = [boundX, boundY]
                    return self.lastCorner
        return None
    
    def highlight(self, curr: Shape):
        self.curr = curr

        for x in [curr.left, curr.right]:
            for y in [curr.top, curr.bottom]:
                self.drawCorner(x, y)
    
    def drawCorner(self, x, y):
        self.cnv.create_rectangle(x-self.padding, y-self.padding, x+self.padding, y+self.padding, fill="black")