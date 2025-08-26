import pymunk as pm
from tkinter import PhotoImage
from tkinter.constants import CENTER

from elements.tool import Tool
from simulation import Simulation
from utils import polar_to_cartesian
from ui.toolManager import ToolManager


class PinJoint(Tool):
    NAME: str = "pin_joint"

    def __init__(self, id):
        Tool.__init__(self, id)
        self.body_a = {
            'body': None, # Body object
            'pos': None, # Body position in world coordinates
            'local_pos': None # Click position in local coordinates
            }
        
        self.body_b = {'body': None, 'pos': None, 'local_pos': None}

        self.mouse_position = None

        self.icon = PhotoImage(
            file="tool_menu_buttons_removed_background_1/pin_joint.png"
            )

    def draw(self, cnv):
        super().draw(cnv)

        # Draw the pin joint icon at any of the two bodies
        body_a = self.body_a

        # Get the local position in polar coordinates
        loc_pos_a = body_a['local_pos'].polar_tuple

        # Convert to cartesian coordinates and rotate by the body's angle
        local_pos_a = polar_to_cartesian(
            (loc_pos_a[0],
            loc_pos_a[1] + body_a['body'].body.angle)
            )
        
        anchor = local_pos_a + body_a['body'].body.position

        cnv.create_image(
            anchor.x, 
            anchor.y, 
            image=self.icon, 
            anchor=CENTER
            )

    def find_parent(self, event):
        element = Simulation().object_at_pos(event)

        if element:
            # In case multiple objects overlap, take the first two
            self.parent = element[:2]
            return True

    def initiate(self, event):
        num_objects = len(Simulation().objects)
        if num_objects < 2:
            print("Not enough objects to create a joint.")
            return False

        elif self.find_parent(event):
            self.mouse_position = event
            self.position = event
            return True

    def initialize(self):
        body_a, body_b = self.parent

        self.body_a['body'] = body_a
        self.body_b['body'] = body_b

        self.body_a['pos'] = body_a.position
        self.body_b['pos'] = body_b.position

        local_pos_a = body_a.body.world_to_local(self.mouse_position)
        local_pos_b = body_b.body.world_to_local(self.mouse_position)

        self.body_a['local_pos'] = local_pos_a
        self.body_b['local_pos'] = local_pos_b
        
        joint = pm.PinJoint(
            a=body_a.body, 
            b=body_b.body,
            anchor_a=local_pos_a,
            anchor_b=local_pos_b,
            )
        
        joint.collide_bodies = False
        
        Simulation().space.add(joint)
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
