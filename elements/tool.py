import pymunk as pm

from abc import abstractmethod
from ui.selection import Selection
from utils import point_inside_rect

class Tool:
    def __init__(self, id):
        self.id = id
        
        # Position data
        self.left: float = None
        self.right: float = None
        self.top: float = None
        self.bottom: float = None

        self.selection = Selection(self)

    @abstractmethod
    def initiate(self, event: pm.Vec2d):
        pass

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def handle_event(self, event: pm.Vec2d):
        pass

    @abstractmethod
    def select(self, event: pm.Vec2d):
        pass

    def point_inside(self, point):
        px, py = point
        return point_inside_rect(self.left, self.top, self.right, self.bottom, px, py)
    
    # def highlight(self):
    #     self.selection.highlight(self)