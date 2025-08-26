import pymunk as pm

from .shape import Shape

from utils import point_inside_rect


class Rectangle(Shape):
    NAME = "rectangle"

    def __init__(self, id:int, mass:float=10.0, friction:float=0.5, elasticity:float=1, body_type:int=pm.Body.DYNAMIC):
        Shape.__init__(self, id, mass, friction, elasticity, body_type)
        self.fill = "lightgreen"

    def place(self, space:pm.Space) -> None:
        super().place(space)

        self.points = [(-self.width/2, -self.height/2), 
                       (self.width/2, -self.height/2), 
                       (self.width/2, self.height/2), 
                       (-self.width/2, self.height/2)]
        
        self.shape = pm.Poly.create_box(self.body, (self.width, self.height))

        self.shape.collision_type = 1
        self.shape.mass = self.mass
        self.shape.friction = self.friction
        self.shape.elasticity = self.elasticity

        if (self.body):
            space.add(self.body, self.shape)

    def draw(self, cnv):
        super().draw(cnv)
        if self.preview:
            cnv.create_rectangle(self.left, 
                                self.top, 
                                self.right, 
                                self.bottom,
                                fill=None)
        else:
            
            points = []
            for v in self.shape.get_vertices():
                points.append(self.body.local_to_world(v))
            
            coords = []
            for p in points:
                coords.extend([p.x, p.y])
            cnv.create_polygon(coords, fill=self.fill, outline="black", width=1)
    
    def point_inside(self, point):
        return point_inside_rect(self.left, self.top, self.right, self.bottom, point.x, point.y)

 