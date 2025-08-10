from tkinter import Canvas
from abc import ABC, abstractmethod
from utils import pointInsideRect, Bound

import pymunk as pm


class Shape(ABC):
    NAME: str = "shape"

    body: pm.Body | None = None
    shape: pm.Shape
    position: pm.Vec2d
    orgPosition: pm.Vec2d
    
    def __init__(self, id : int, mass : float=10.0, friction : float=0.5, elasticity : float=0.5, body_type : int=pm.Body.DYNAMIC):
        self.fill: str = "red"
        self.preview: bool = False
        
        self.id = id
        self.mass = mass
        self.friction = friction
        self.elasticity = elasticity
        self.body_type = body_type
        self.z_index = 0

        self.body_type = body_type
        
        # Position data
        self.left: float = None
        self.right: float = None
        self.top: float = None
        self.bottom: float = None
    
    def resize(self, boundX: Bound, boundY: Bound, newX, newY):
        if boundX == Bound.LEFT:
            self.left = newX
        if boundX == Bound.RIGHT:
            self.right = newX
        if boundY == Bound.TOP:
            self.top = newY
        if boundY == Bound.BOTTOM:
            self.bottom = newY

    def if_valid(self):
        return self.left != self.right and self.top != self.bottom
    
    def move(self, offset: pm.Vec2d):
        self.left += offset.x
        self.right += offset.x
        self.top += offset.y
        self.bottom += offset.y
    
    def update(self):
        # The amount moved
        offset = self.body.position - self.position

        self.move(offset)

        self.position = self.body.position
    
    @abstractmethod
    def draw(self, cnv: Canvas):
        pass

    @abstractmethod
    def place(self, space: pm.Space):
        self.body = pm.Body(body_type=self.body_type)
        self.position = pm.Vec2d((self.right + self.left) / 2, (self.top + self.bottom) / 2)
        self.orgPosition = pm.Vec2d((self.right + self.left) / 2, (self.top + self.bottom) / 2)
        self.body.position = self.position
    
    def reset(self) -> None:
        self.body.position = self.orgPosition
        self.body.angle = 0
        self.body.velocity = (0, 0)
        self.body.angular_velocity = 0

    def pointInside(self, point):
        px, py = point
        return pointInsideRect(self.left, self.top, self.right, self.bottom, px, py)
    
    def fixOrientation(self):
        # If the sides are opposite
        if self.left > self.right:
            self.left, self.right = self.right, self.left
        if self.top > self.bottom:
            self.bottom, self.top = self.top, self.bottom