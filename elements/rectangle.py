from elements import Shape

import pymunk as pm


class Rectangle(Shape):
    NAME = "rectangle"

    def __init__(self, id:int, mass:float=10.0, friction:float=0.5, elasticity:float=0.5, body_type:int=pm.Body.DYNAMIC):
        Shape.__init__(self, id, mass, friction, elasticity, body_type)
        self.fill = "lightgreen"

    def draw(self, cnv):
        cnv.create_rectangle(self.left, 
                            self.top, 
                            self.right, 
                            self.bottom, 
                            fill=None if self.preview else self.fill)