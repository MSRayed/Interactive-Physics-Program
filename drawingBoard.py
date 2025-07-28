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

        self.mouseRecordedPos: Vec2d = None

        # Flags
        self.creationFlag: bool = False

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
                self.mouseRecordedPos = Vec2d(event.x, event.y)
                return
        
        # If mouse not on any other element, than create a new one
        self.creationFlag = True
        self.currentElement = shape.Oval()
        self.elements.append(self.currentElement)

        self.currentElement.initiate(Vec2d(event.x, event.y))
        self.currentElement.preview = True
    
    @queue_redraw
    def leftMouseMotion(self, event):
        mousePos = Vec2d(event.x, event.y)

        if self.creationFlag:
            self.currentElement.release(mousePos)
        else:
            if self.currentElement:                
                offset = mousePos - self.mouseRecordedPos

                # Delete the last drawn before drawing moved element
                self.currentElement.move(offset)
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

    def redraw(self):
        self.delete("all")
        
        for element in self.elements:
            element.draw(self)
        
        if self.currentElement: 
            self.selection.highlight(self.currentElement)


class Selection:
    def __init__(self, cnv: Canvas):
        self.cnv = cnv
        self.padding = 3
        self.curr = None
        self
    
    def getMouseOnCorner(mouse: Vec2d):
        pass
    
    def highlight(self, curr: shape.Shape):
        self.curr = curr

        self.drawCorner(curr.left, curr.top)
        self.drawCorner(curr.right, curr.top)
        self.drawCorner(curr.left, curr.bottom)
        self.drawCorner(curr.right, curr.bottom)
    
    def drawCorner(self, x, y):
        self.cnv.create_rectangle(x-self.padding, y-self.padding, x+self.padding, y+self.padding, fill="black")