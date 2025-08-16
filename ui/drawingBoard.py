from tkinter import Canvas
from pymunk.vec2d import Vec2d

from ui.toolManager import ToolManager
from utils import Singleton
from simulation import Simulation

from random import randint


class DrawingBoard(Canvas, metaclass=Singleton):
    def __init__(self, root=None, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.root = root

        self.bind("<Button-1>", self.left_click)
        self.bind("<B1-Motion>", self.left_mouse_motion)
        self.bind("<ButtonRelease-1>", self.left_mouse_release)

        self.currentElement = None

        # Register redraw callback with simulation
        sim = Simulation()
        sim.register_observer(self.schedule_redraw)

    def schedule_redraw(self):
        self.root.after(0, self.redraw)

    def queue_redraw(func):
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.redraw()
        return wrapper
    
    def left_click(self, event):
        for element in Simulation().objects:
            if element.point_inside(Vec2d(event.x, event.y)):
                self.currentElement = element
                self.currentElement.select(Vec2d(event.x, event.y))
                return
        
        # Creating shapes
        if ToolManager().currentTool:
            # If mouse not on any other element, than create a new one
            self.creationFlag = True

            self.currentElement = ToolManager().currentTool(randint(0, 10000))

            self.currentElement.initiate(Vec2d(event.x, event.y))
    
    @queue_redraw
    def left_mouse_motion(self, event):
        mousePos = Vec2d(event.x, event.y)

        self.currentElement.handle_event(mousePos)

    @queue_redraw
    def left_mouse_release(self, _):
        if self.currentElement:
            self.currentElement.initialize()
            Simulation().add_object(self.currentElement)
        else:
            self.currentElement = None

    def redraw(self):        
        self.delete("all")
        
        if self.currentElement: self.currentElement.draw(self)

        for element in Simulation().objects:
            element.draw(self)