from __future__ import annotations
from typing import TYPE_CHECKING

from tkinter import Canvas
from abc import ABC, abstractmethod
from utils import Bound, point_inside_rect

from elements.tool import Tool

import pymunk as pm

if TYPE_CHECKING:
    from .anchor import Anchor


class Shape(ABC, Tool):
    NAME: str = "shape"

    body: pm.Body | None = None
    shape: pm.Shape
    
    def __init__(self, id : int, mass : float=10.0, friction : float=0.5, elasticity : float=0.5, body_type : int=pm.Body.DYNAMIC):
        Tool.__init__(self, id)

        self.fill: str
        self.preview: bool = False
        
        self.mass = mass
        self.friction = friction
        self.elasticity = elasticity
        self.body_type = body_type
        self.z_index = 0

        self.creationFlag = False
        self.mouseOnCorner = None

        self.mouseRecordedPos = None

        self.anchor: Anchor = None

        self.width: float = 0
        self.height: float = 0

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
        
        self.width = abs(self.right - self.left)
        self.height = abs(self.bottom - self.top)
        self.position = pm.Vec2d((self.left + self.right)/2, (self.top + self.bottom)/2)
        
        if self.body:
            self.reset()

    def if_valid(self):
        return self.left != self.right and self.top != self.bottom
    
    def move(self, offset: pm.Vec2d):
        self.left += offset.x
        self.right += offset.x
        self.top += offset.y
        self.bottom += offset.y

        self.position += offset
        self.body.position = self.position

        if self.anchor: self.anchor.move(offset)
    
    def point_inside_bounds(self, point):
        return point_inside_rect(self.left-self.cornerSize, self.top-self.cornerSize, self.right+self.cornerSize, self.bottom+self.cornerSize, point.x, point.y)
    
    def update(self):
        pass
    
    @abstractmethod
    def draw(self, cnv: Canvas):
        pass

    def place(self, space: pm.Space):
        self.body = pm.Body(body_type=self.body_type)
        self.position = pm.Vec2d((self.right + self.left) / 2, (self.top + self.bottom) / 2)
        self.body.position = self.position
    
    def reset(self):
        self.body.position = self.position
        self.body.angle = 0
        self.body.velocity = (0, 0)
        self.body.angular_velocity = 0
    
    def fix_orientation(self):
        # If the sides are opposite
        if self.left > self.right:
            self.left, self.right = self.right, self.left
        if self.top > self.bottom:
            self.bottom, self.top = self.top, self.bottom
    
    def get_mouse_on_corner(self, mouse: pm.Vec2d):
        for (x, boundX) in zip([self.left, self.right], [Bound.LEFT, Bound.RIGHT]):
            for (y, boundY) in zip([self.top, self.bottom], [Bound.TOP, Bound.BOTTOM]):
                if point_inside_rect(x-self.cornerSize, y-self.cornerSize, x+self.cornerSize, y+self.cornerSize, mouse.x, mouse.y):
                    print([boundX, boundY])
                    return [boundX, boundY]
        return None
    
    def initiate(self, event, _):
        # If mouse not on any other element, than create a new one
        self.creationFlag = True

        # Fixing the top left when creating
        self.left = event.x
        self.top = event.y

        self.preview = True

        return True

    def click_event(self, event):
        self.mouseRecordedPos = event

        if self.get_mouse_on_corner(event):
            self.mouseOnCorner = self.get_mouse_on_corner(event)        
    
    def motion_event(self, event):
        if self.creationFlag:
            self.resize(Bound.RIGHT, Bound.BOTTOM, event.x, event.y)
            pass
        else:
            if self.mouseOnCorner:
                self.resize(*self.mouseOnCorner, event.x, event.y)
                return
            
            offset = event - self.mouseRecordedPos

            self.move(offset)

            self.mouseRecordedPos = event
    
    def release_event(self):
        self.mouseOnCorner = None
    
    def initialize(self):
        if self.creationFlag:
            if self.if_valid():
                self.preview = False
                self.creationFlag = False

        # Check for the orientation and fix if opposite
        self.fix_orientation()
    
    def delete(self, space: pm.Space):        
        if self.shape and self.shape in space.shapes:
            space.remove(self.shape)
            self.shape = None  # optional: clear reference

        if self.body and self.body in space.bodies:
            space.remove(self.body)
            self.body = None  # optional: clear reference