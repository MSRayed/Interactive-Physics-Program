from utils import Bound
from elements import Shape

import pymunk as pm


class Circle(Shape):
    NAME = "circle"

    def __init__(self, id:int, mass:float=10.0, friction:float=0.5, elasticity:float=0.5, body_type:int=pm.Body.DYNAMIC):
        Shape.__init__(self, id, mass, friction, elasticity, body_type)
        self.fill = "red"
    
    def place(self, space:pm.Space) -> None:
        super().place(space)

        self.radius = (self.right - self.left) / 2
        self.shape = pm.Circle(self.body, self.radius)
        # self.shape.group_id = self.group_id
        self.shape.collision_type = 1
        self.shape.mass = self.mass
        self.shape.friction = self.friction
        self.shape.elasticity = self.elasticity

        if (self.body):
            space.add(self.body, self.shape)
    
    def resize(self, boundX, boundY, newX, newY):
        if boundX == Bound.LEFT:
            anchor_x = self.right
            dx = anchor_x - newX
        elif boundX == Bound.RIGHT:
            anchor_x = self.left
            dx = newX - anchor_x
        else:
            dx = 0

        if boundY == Bound.TOP:
            anchor_y = self.bottom
            dy = anchor_y - newY
        elif boundY == Bound.BOTTOM:
            anchor_y = self.top
            dy = newY - anchor_y
        else:
            dy = 0

        # Choose the smaller of dx and dy to maintain a square
        size = min(abs(dx), abs(dy))

        # Reapply size based on direction of resizing
        if boundX == Bound.LEFT:
            self.left = self.right - size * (1 if dx >= 0 else -1)
        elif boundX == Bound.RIGHT:
            self.right = self.left + size * (1 if dx >= 0 else -1)

        if boundY == Bound.TOP:
            self.top = self.bottom - size * (1 if dy >= 0 else -1)
        elif boundY == Bound.BOTTOM:
            self.bottom = self.top + size * (1 if dy >= 0 else -1)
    

    def draw(self, cnv):
        super().draw(cnv)
        cnv.create_oval(self.left, 
                        self.top, 
                        self.right, 
                        self.bottom, 
                        fill=None if self.preview else self.fill)