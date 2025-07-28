from tkinter import Canvas
from elements import shape
from pymunk.vec2d import Vec2d

from typing import List


class DrawingBoard(Canvas):
    def __init__(self, root, *args, **kwargs):
        Canvas.__init__(self, root, *args, **kwargs)

        self.bind("<Button-1>", self.leftClick)
        self.bind("<B1-Motion>", self.leftMouseMotion)
        self.bind("<ButtonRelease-1>", self.leftMouseRelease)

        self.elements: List[shape.Shape] = []
        self.currentElement = None
        self.lastDrawn = None

        # Flags
        self.creationFlag: bool = False
        self.finalizeFlag: bool = False

        self.selection = Selection(self)

    def queue_redraw(func):
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.redraw()
        return wrapper
    
    def leftClick(self, event):
        for element in self.elements:
            if element.pointInside(Vec2d(event.x, event.y)):
                self.currentElement = element
                return
        
        # If mouse not on any other element, than create a new one
        self.creationFlag = True
        self.currentElement = shape.Oval()
        self.elements.append(self.currentElement)

        self.currentElement.initiate(Vec2d(event.x, event.y))
        self.currentElement.preview = True
    
    @queue_redraw
    def leftMouseMotion(self, event):
        if self.creationFlag:
            self.currentElement.release(Vec2d(event.x, event.y))

    @queue_redraw
    def leftMouseRelease(self, _):
        if self.creationFlag:
            self.currentElement.preview = False
            self.finalizeFlag = True
            self.creationFlag = False
        
        self.selection.highlight(self.currentElement)

    def redraw(self):
        if self.currentElement:
            self.delete(self.lastDrawn)
            
            if self.finalizeFlag:
                # Draw once to finalize the element so the last version doesn't get deleted
                self.lastDrawn = self.currentElement.draw(self)
                self.finalizeFlag = False
            
            self.lastDrawn = self.currentElement.draw(self)


class Selection:
    def __init__(self, cnv: Canvas):
        self.lastDrawn = None
        self.cnv = cnv
        self.curr = None
    
    def highlight(self, curr: shape.Shape):
        self.curr = curr
        self.cnv.delete(self.lastDrawn)
        self.lastDrawn = self.cnv.create_rectangle(curr.get_left_boundary()-3, curr.get_top_boundary()-3, curr.get_right_boundary()+3, curr.get_bottom_boundary()+3)