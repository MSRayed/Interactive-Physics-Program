import pymunk as pm

from tkinter import PhotoImage
from tkinter.constants import CENTER

from .tool import Tool
from .shape import Shape

from simulation import Simulation


class Anchor(Tool):
    def __init__(self, id):
        Tool.__init__(self, id)
        self.parent = None

        self.icon = PhotoImage(file="tool_menu_buttons_removed_background_1/anchor.png")
    
    def draw(self, cnv):
        super().draw(cnv)
        cnv.create_image(self.position.x, self.position.y, image=self.icon, anchor=CENTER)

    def initiate(self, event):
        for element in Simulation().objects:
            if element.point_inside(event) and isinstance(element, Shape):
                if not element.anchor:
                    self.parent = element
                    self.position = event
                    self.orgPosition = event
                    return True
                else:
                    pass
        return False

    def initialize(self):
        self.parent.anchor = self
        self.parent.body.body_type = pm.Body.KINEMATIC
    
    def move(self, offset):
        self.position += offset
    
    def reset(self):
        pass