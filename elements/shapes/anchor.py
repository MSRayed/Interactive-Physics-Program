import pymunk as pm

from tkinter import PhotoImage
from tkinter.constants import CENTER

from ..tool import Tool

from simulation import Simulation
from ui.toolManager import ToolManager


class Anchor(Tool):
    def __init__(self, id):
        Tool.__init__(self, id)
        self.parent = None

        self.icon = PhotoImage(file="tool_menu_buttons_removed_background_1/anchor.png")
    
    def draw(self, cnv):
        super().draw(cnv)
        cnv.create_image(self.position.x, self.position.y, image=self.icon, anchor=CENTER)
    
    def find_parent(self, event):
        result = Simulation().object_at_pos(event)

        # Normalize to list
        if not result:
            return False
        if not isinstance(result, list):
            elements = [result]
        else:
            elements = result

        # Filter out self
        elements = [el for el in elements if el is not self]

        if elements:
            element = elements[0]
            if not element.anchor:
                if self.parent:
                    # Reset the older parent
                    self.parent.body.body_type = pm.Body.DYNAMIC
                    self.parent.anchor = None
                    self.parent = None

                self.parent = element
                return True

        return False

    def initiate(self, event, _):
        if self.find_parent(event):
            self.position = event
            return True
        return False

    def initialize(self):
        self.parent.anchor = self
        self.parent.body.body_type = pm.Body.KINEMATIC
        ToolManager().clear()
    
    def move(self, offset):
        self.position += offset

    def motion_event(self, event):
        offset = event - self.mouseRecordedPos

        self.move(offset)

        self.mouseRecordedPos = event

        # To be improved later
        if self.find_parent(self.position):
            self.initialize()

    def click_event(self, event):
        self.mouseRecordedPos = event
    
    def reset(self):
        pass

    def delete(self, space: pm.Space):
        self.parent.body.body_type = pm.Body.DYNAMIC
        self.parent.anchor = None
        self.parent = None
