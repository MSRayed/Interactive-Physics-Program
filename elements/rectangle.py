from elements import Shape

import pymunk as pm


class Rectangle(Shape):
    NAME = "rectangle"

    def __init__(self, id:int, mass:float=10.0, friction:float=0.5, elasticity:float=0.5, body_type:int=pm.Body.DYNAMIC):
        Shape.__init__(self, id, mass, friction, elasticity, body_type)
        self.fill = "lightgreen"
    
    def place(self, space:pm.Space) -> None:
        super().place(space)

        self.points = [(self.left, self.top), (self.right, self.top), (self.right, self.bottom), (self.left, self.bottom)]
        self.shape = pm.shapes.Poly(self.body, self.points)
        # self.shape.group_id = self.group_id
        self.shape.collision_type = 1
        self.shape.mass = self.mass
        self.shape.friction = self.friction
        self.shape.elasticity = self.elasticity

        if (self.body):
            space.add(self.body, self.shape)

    def draw(self, cnv):
        super().draw(cnv)
        cnv.create_rectangle(self.left, 
                            self.top, 
                            self.right, 
                            self.bottom, 
                            fill=None if self.preview else self.fill)