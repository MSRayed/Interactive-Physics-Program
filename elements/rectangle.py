from elements import Shape

import pymunk as pm


class Rectangle(Shape):
    NAME = "rectangle"

    def __init__(self, id:int, mass:float=10.0, friction:float=0.5, elasticity:float=0.5, body_type:int=pm.Body.DYNAMIC):
        Shape.__init__(self, id, mass, friction, elasticity, body_type)
        self.fill = "lightgreen"
    
    def place(self, space:pm.Space) -> None:
        super().place(space)

        self.points = [(-self.width/2, -self.height/2), (self.width/2, -self.height/2), (self.width/2, self.height/2), (-self.width/2, self.height/2)]
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
        super().draw(cnv)
        if self.preview:
            cnv.create_rectangle(self.left, 
                            self.top, 
                            self.right, 
                            self.bottom,
                            fill=None)
        else:
            cnv.create_rectangle(self.body.position.x - self.width/2, 
                                self.body.position.y - self.height/2,
                                self.body.position.x + self.width/2, 
                                self.body.position.y + self.height/2, 
                                fill=self.fill)