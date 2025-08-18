import pymunk as pm

from tkinter import PhotoImage

from ..parentedTool import ParentedTool
from .shape import Shape

from simulation import Simulation


class Anchor(ParentedTool):
    def __init__(self, id):
        ParentedTool.__init__(self, id)
        self.parent = None

        self.icon = PhotoImage(file="tool_menu_buttons_removed_background_1/anchor.png")
    
    def find_parent(self, event):
        element = Simulation().object_at_pos(event, Shape)
        if element:
            if not element.anchor:
                if self.parent:
                    # Reset the older parent
                    self.parent.body.body_type = pm.Body.DYNAMIC
                
                self.parent = element
                return True

    def initialize(self):
        self.parent.anchor = self
        self.parent.body.body_type = pm.Body.KINEMATIC