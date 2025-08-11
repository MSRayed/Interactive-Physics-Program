import pymunk as pm

from elements import Shape

class Anchor:
    @staticmethod
    def act(shape: Shape):
        shape.body.body_type = pm.Body.STATIC