from tkinter import Canvas
from elements import shapes
from pymunk.vec2d import Vec2d


class DrawingBoard(Canvas):
    def __init__(self, root, *args, **kwargs):
        Canvas.__init__(self, root, *args, **kwargs)

        self.bind("<Button-1>", self.leftClick)
        self.bind("<B1-Motion>", self.leftMouseMotion)
        self.bind("<ButtonRelease-1>", self.leftMouseRelease)

        self.currentElement = None
        self.lastDrawn = None

    def queue_redraw(func):
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.redraw()
        return wrapper
    
    def leftClick(self, event):
        self.currentElement = shapes.Square()
        self.currentElement.initiate(Vec2d(event.x, event.y))
        self.currentElement.preview = True
    
    @queue_redraw
    def leftMouseMotion(self, event):
        self.currentElement.release(Vec2d(event.x, event.y))

    @queue_redraw
    def leftMouseRelease(self, event):
        self.currentElement.release(Vec2d(event.x, event.y))

    def redraw(self):
        if self.currentElement:
            self.delete(self.lastDrawn)
            self.lastDrawn = self.currentElement.draw(self)