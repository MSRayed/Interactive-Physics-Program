from tkinter import Canvas
from pymunk.vec2d import Vec2d
from typing import List

from elements.shape import Shape
from shapePanel import ShapePanel
from selection import Selection
from utils import Bound


class DrawingBoard(Canvas):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.bind("<Button-1>", self.leftClick)
        self.bind("<B1-Motion>", self.leftMouseMotion)
        self.bind("<ButtonRelease-1>", self.leftMouseRelease)

        self.elements: List[Shape] = []
        self.currentElement = None

        self.mouseRecordedPos: Vec2d = None

        # Flags
        self.creationFlag: bool = False
        self.resizingFlag: bool = False

        self.selection = Selection(self)

    def queue_redraw(func):
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.redraw()
        return wrapper
    
    def leftClick(self, event):
        if self.selection.getMouseOnCorner(Vec2d(event.x, event.y)):
            self.resizingFlag = True
            return

        for element in self.elements:
            if element.pointInside(Vec2d(event.x, event.y)):
                self.currentElement = element
                self.mouseRecordedPos = Vec2d(event.x, event.y)
                return
        
        # If mouse not on any other element, than create a new one
        self.creationFlag = True

        self.currentElement = ShapePanel().selectedShape()        
        self.elements.append(self.currentElement)

        # Fixing the top left when creating
        self.currentElement.left = event.x
        self.currentElement.top = event.y

        self.currentElement.preview = True
    
    @queue_redraw
    def leftMouseMotion(self, event):
        mousePos = Vec2d(event.x, event.y)

        if self.creationFlag:
            self.currentElement.resize(Bound.RIGHT, Bound.BOTTOM, event.x, event.y)
        else:
            if self.currentElement:                
                if self.resizingFlag:
                    self.currentElement.resize(*self.selection.lastCorner, event.x, event.y)
                    return
                
                offset = mousePos - self.mouseRecordedPos

                # Delete the last drawn before drawing moved element
                self.currentElement.left += offset.x
                self.currentElement.right += offset.x
                self.currentElement.top += offset.y
                self.currentElement.bottom += offset.y

                self.mouseRecordedPos = mousePos


    @queue_redraw
    def leftMouseRelease(self, _):
        if self.creationFlag:
            if self.currentElement.if_valid():
                self.currentElement.preview = False
                self.creationFlag = False
            else:
                self.elements.remove(self.currentElement)
                self.currentElement = None
        
        if self.resizingFlag:
            self.resizingFlag = False

    def redraw(self):
        self.delete("all")
        
        for element in self.elements:
            element.draw(self)
        
        if self.currentElement: 
            self.selection.highlight(self.currentElement)