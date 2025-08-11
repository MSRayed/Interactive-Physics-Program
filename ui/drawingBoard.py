from tkinter import Canvas
from pymunk.vec2d import Vec2d

from ui.shapePanel import ShapePanel
from ui.selection import Selection
from ui.toolManager import ToolManager
from utils import Bound, Singleton
from simulation import Simulation
from elements import Shape, Anchor

from random import randint


class DrawingBoard(Canvas, metaclass=Singleton):
    def __init__(self, root=None, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.root = root

        self.bind("<Button-1>", self.left_click)
        self.bind("<B1-Motion>", self.left_mouse_motion)
        self.bind("<ButtonRelease-1>", self.left_mouse_release)

        self.currentElement = None

        self.mouseRecordedPos: Vec2d = None

        # Flags
        self.creationFlag: bool = False
        self.resizingFlag: bool = False

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
        if self.selection.get_mouse_on_corner(Vec2d(event.x, event.y)):
            self.resizingFlag = True
            return

        for element in Simulation().objects:
            if element.point_inside(Vec2d(event.x, event.y)):
                self.currentElement = element
                self.mouseRecordedPos = Vec2d(event.x, event.y)

                if ToolManager().currentTool is Anchor:
                    print("Anchoring", self.currentElement)
                    Anchor.act(self.currentElement)

                return
        
        # Creating shapes
        if issubclass(ToolManager().currentTool, Shape):
            # If mouse not on any other element, than create a new one
            self.creationFlag = True

            self.currentElement = ShapePanel().selectedShape(randint(0, 10000))

            # Fixing the top left when creating
            self.currentElement.left = event.x
            self.currentElement.top = event.y

            self.currentElement.preview = True
    
    @queue_redraw
    def left_mouse_motion(self, event):
        mousePos = Vec2d(event.x, event.y)

        if self.creationFlag and self.currentElement:
            self.currentElement.resize(Bound.RIGHT, Bound.BOTTOM, event.x, event.y)
        else:
            if self.currentElement:                
                if self.resizingFlag:
                    self.currentElement.resize(*self.selection.lastCorner, event.x, event.y)
                    return
                
                offset = mousePos - self.mouseRecordedPos

                self.currentElement.move(offset)

                self.mouseRecordedPos = mousePos

    @queue_redraw
    def left_mouse_release(self, _):
        if self.creationFlag:
            if self.currentElement.if_valid():
                self.currentElement.preview = False
                self.creationFlag = False
                Simulation().add_object(self.currentElement)
                ShapePanel().clear_selection()
            else:
                self.currentElement = None
        
        if self.resizingFlag:
            self.resizingFlag = False

        if self.currentElement:
            # Check for the orientation and fix if opposite
            self.currentElement.fix_orientation()

    def redraw(self):        
        self.delete("all")
        
        if self.currentElement: self.currentElement.draw(self)

        for element in Simulation().objects:
            element.draw(self)
        
        if self.currentElement: 
            self.selection.highlight(self.currentElement)