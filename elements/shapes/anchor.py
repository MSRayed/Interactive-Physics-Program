import pymunk as pm

from tkinter import PhotoImage
from tkinter.constants import CENTER

from ..tool import Tool
from .shape import Shape

from utils import point_in_circle
from simulation import Simulation


class Anchor(Tool):
    def __init__(self, id):
        Tool.__init__(self, id)
        self.parent = None

        self.icon = PhotoImage(file="tool_menu_buttons_removed_background_1/anchor.png")
    
    def draw(self, cnv):
        super().draw(cnv)
        cnv.create_image(self.position.x, self.position.y, image=self.icon, anchor=CENTER)
    
    def find_parent(self, event):
        element = Simulation().object_at_pos(event, Shape)
        if element:
            if not element.anchor:
                if self.parent:
                    # Reset the older parent
                    self.parent.body.body_type = pm.Body.DYNAMIC
                
                self.parent = element
                return True

    def initiate(self, event):
        if self.find_parent(event):
            self.position = event
            return True
        return False

    def initialize(self):
        self.parent.anchor = self
        self.parent.body.body_type = pm.Body.KINEMATIC
    
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

    def point_inside(self, point):
        px, py = point
        return point_in_circle(px, py, self.position.x, self.position.y, self.cornerSize * 2)
    
    def reset(self):
        pass