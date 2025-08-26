from typing import List

import pymunk as pm
from random import randint
from tkinter import PhotoImage
from tkinter.constants import CENTER

from elements.tool import Tool
from simulation import Simulation
from utils import polar_to_cartesian
from ui.toolManager import ToolManager


class RigidJoint(Tool):
    NAME: str = "rigid_joint"

    def __init__(self, id):
        Tool.__init__(self, id)
        self.body_a = {
            'body': None, # Body object
            'pos': None, # Body position in world coordinates
            'local_pos': None # Click position in local coordinates
            }
        
        self.joints: List[pm.Constraint] = []
        
        self.body_b = {'body': None, 'pos': None, 'local_pos': None}

        self.mouse_position = None

        self.icon = PhotoImage(
            file="tool_menu_buttons_removed_background_1/rigid_joint.png"
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
            self.parent = element
            return True

    def initiate(self, event, at_center):
        num_objects = len(Simulation().objects)
        if num_objects < 2:
            print("Not enough objects to create a joint.")
            return False

        elif self.find_parent(event):
            if at_center:
                self.position = self.parent[0].position
                self.mouse_position = self.parent[0].position
            else:
                self.position = event
                self.mouse_position = event
            return True

    def initialize(self):

        body_a, body_b, *body_n = self.parent

        # If there are more than 2 bodies, make them a collision group
        if body_n:
            group_id = randint(1, 1000000)
            for body in [body_a, body_b, *body_n]:

                body.shape.filter = pm.ShapeFilter(
                    group=group_id
                    )
        
        self.body_a['body'] = body_a
        self.body_b['body'] = body_b

        self.body_a['pos'] = body_a.position
        self.body_b['pos'] = body_b.position

        local_pos_a = body_a.body.world_to_local(self.mouse_position)
        local_pos_b = body_b.body.world_to_local(self.mouse_position)

        self.body_a['local_pos'] = local_pos_a
        self.body_b['local_pos'] = local_pos_b

        joint1 = pm.PinJoint(
            a=body_a.body, 
            b=body_b.body,
            anchor_a=local_pos_a,
            anchor_b=local_pos_b
            )
        
        joint2 = pm.RotaryLimitJoint(
            a=body_b.body, 
            b=body_a.body,
            min=0, 
            max=0
            )
        
        self.joints.append(joint1)
        self.joints.append(joint2)

        joint1.collide_bodies = False
        joint2.collide_bodies = False

        Simulation().space.add(joint1, joint2)
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
        # Check if the joint exists in the space
        for joint in self.joints:
            if joint in space.constraints:
                space.remove(joint)
                self.joint = None