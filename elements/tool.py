import pymunk as pm

from abc import abstractmethod


class Tool:
    cornerSize = 3
    position: pm.Vec2d

    def __init__(self, id):
        self.id = id
        self.mouseRecordedPos = None

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def place(self, space: pm.Space):
        pass

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
    def draw(self, cnv):
        pass

    @abstractmethod
    def move(self, offset: pm.Vec2d):
        pass

    @abstractmethod
    def point_inside(self, point):
        pass