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
            self.currentElement.preview = False
            self.creationFlag = False

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
    
    def highlight(self, curr: shape.Shape):
        self.curr = curr

        left = curr.get_left_boundary()
        top = curr.get_top_boundary()
        right = curr.get_right_boundary()
        bottom = curr.get_bottom_boundary()

        self.cnv.create_rectangle(left-self.padding, top-self.padding, left+self.padding, top+self.padding, fill="black")
        self.cnv.create_rectangle(right-self.padding, top-self.padding, right+self.padding, top+self.padding, fill="black")
        self.cnv.create_rectangle(left-self.padding, bottom-self.padding, left+self.padding, bottom+self.padding, fill="black")
        self.cnv.create_rectangle(right-self.padding, bottom-self.padding, right+self.padding, bottom+self.padding, fill="black")