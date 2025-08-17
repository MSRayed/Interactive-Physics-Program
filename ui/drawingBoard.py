from tkinter import Canvas
from pymunk.vec2d import Vec2d

from ui.toolManager import ToolManager
from utils import Singleton
from simulation import Simulation

from ui.selection import Selection

from random import randint


class DrawingBoard(Canvas, metaclass=Singleton):
    def __init__(self, root=None, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.root = root

        self.bind("<Button-1>", self.left_click)
        self.bind("<B1-Motion>", self.left_mouse_motion)
        self.bind("<ButtonRelease-1>", self.left_mouse_release)

        self.currentElement = None

        self.tempElement = None

        self.selection = Selection(self)

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
        mousePos = Vec2d(event.x, event.y)

        if not ToolManager().currentTool:
            for element in Simulation().objects:
                if element.point_inside(mousePos):
                    self.currentElement = element
                    self.currentElement.click_event(mousePos)
                    return
        
        # Creating shapes
        if ToolManager().currentTool:
            # If mouse not on any other element, than create a new one
            self.tempElement = ToolManager().currentTool(randint(0, 10000))

            success = self.tempElement.initiate(Vec2d(event.x, event.y))

            if not success: 
                self.tempElement = None
            else:
                self.creationFlag = True
    
    @queue_redraw
    def left_mouse_motion(self, event):
        mousePos = Vec2d(event.x, event.y)

        if self.tempElement:
            self.tempElement.motion_event(mousePos)
            return
        
        self.currentElement.motion_event(mousePos)

    @queue_redraw
    def left_mouse_release(self, _):        
        if self.tempElement:
            self.tempElement.initialize()
            print(self.tempElement)
            Simulation().add_object(self.tempElement)
            self.tempElement, self.currentElement = None, self.tempElement

            ToolManager().clear()
        else:
            self.tempElement = None
        
        if self.currentElement:
            self.currentElement.release_event()

    def redraw(self):        
        self.delete("all")
        
        if self.tempElement: self.tempElement.draw(self)

        for element in Simulation().objects:
            element.draw(self)
        
        # if self.currentElement: self.selection.highlight(self.currentElement)