import pymunk as pm

from abc import abstractmethod
from utils import point_inside_rect

class Tool:
    cornerSize = 3

    def __init__(self, id):
        self.id = id
        
        # Position data
        self.left: float = None
        self.right: float = None
        self.top: float = None
        self.bottom: float = None

    @abstractmethod
    def initiate(self, event: pm.Vec2d):
        pass

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def click_event(self, event: pm.Vec2d):
        pass

    @abstractmethod
    def motion_event(self, event: pm.Vec2d):
        pass

    @abstractmethod
    def release_event(self):
        pass

    @abstractmethod
    def select(self, event: pm.Vec2d):
        pass

    @abstractmethod
    def draw(self, cnv):
        pass

    @abstractmethod
    def point_inside(self, point):
        px, py = point
        return point_inside_rect(self.left-self.cornerSize, self.top-self.cornerSize, self.right+self.cornerSize, self.bottom+self.cornerSize, px, py)