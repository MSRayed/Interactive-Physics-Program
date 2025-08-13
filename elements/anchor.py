import pymunk as pm

from elements import Shape
from elements.tool import Tool


class Anchor(Tool):
    def act(shape: Shape):
        if (not shape.anchored):
            print("Anchoring", shape)
            shape.body.body_type = pm.Body.STATIC
            shape.anchored = True
        else:
            print("Unanchoring", shape)
            shape.body.body_type = pm.Body.DYNAMIC
            shape.anchored = False