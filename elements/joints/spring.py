from math import hypot

import pymunk as pm
from tkinter import PhotoImage

from elements.tool import Tool
from simulation import Simulation
from utils import Singleton, polar_to_cartesian
from ui.toolManager import ToolManager


class Spring(Tool, metaclass=Singleton):
    NAME: str = "spring"

    def __init__(self, id):
        Tool.__init__(self, id)
        self.body_a = {
            'body': None, # Body object
            'pos': None, # Body position in world coordinates
            'local_pos': None # Click position in local coordinates
            }
        
        self.joint: pm.Constraint = None
        
        self.body_b = {'body': None, 'pos': None, 'local_pos': None}

        self.mouse_position = None

        self.icon = PhotoImage(
            file="tool_menu_buttons_removed_background_1/spring.png"
            )

    def draw(self, cnv):
        super().draw(cnv)

        body_a, body_b = self.body_a, self.body_b

        if body_b['body'] is None:
            return

        loc_pos_a = body_a['local_pos'].polar_tuple
        loc_pos_b = body_b['local_pos'].polar_tuple

        local_pos_a = polar_to_cartesian(
            (loc_pos_a[0],
            loc_pos_a[1] + body_a['body'].body.angle)
            )
        
        local_pos_b = polar_to_cartesian(
            (loc_pos_b[0],
            loc_pos_b[1] + body_b['body'].body.angle)
            )

        anchor_a = local_pos_a + body_a['body'].body.position
        anchor_b = local_pos_b + body_b['body'].body.position

        self.draw_spring(
            cnv, 
            anchor_a.x, 
            anchor_a.y, 
            anchor_b.x, 
            anchor_b.y
            )
    
    def find_parent(self, event):
        element = Simulation().object_at_pos(event)

        if element:
            self.parent = element
            
            # if multiple bodies are piled up, select the top one
            if type(self.parent) is list:
                self.parent = self.parent[0]
            return True

    def initiate(self, event, at_center):
        num_objects = len(Simulation().objects)
        if num_objects < 2:
            print("Not enough objects to create a joint.")
            return False

        elif self.find_parent(event):
            if at_center:
                self.position = self.parent.position
                self.mouse_position = self.parent.position
            else:
                self.position = event
                self.mouse_position = event
            return True

    def initialize(self):
        # if multiple bodies are piled up, select the top one
        if type(self.parent) is list:
            self.parent = self.parent[0]
            
        body = self.parent

        if not self.body_a['body']:

            self.body_a['body'] = body
            self.body_a['pos'] = body.position
            
            local_pos_a = body.body.world_to_local(self.mouse_position)

            self.body_a['local_pos'] = local_pos_a

        elif not self.body_b['body']:

            self.body_b['body'] = body
            self.body_b['pos'] = body.position
            
            local_pos_b = body.body.world_to_local(self.mouse_position)
            
            self.body_b['local_pos'] = local_pos_b

            rest_length = (
                self.body_a['pos'] 
                + self.body_a['local_pos'] 
                -  self.body_b['pos'] 
                - self.body_b['local_pos']
                ).length * 0.8
            
            stiffness = 1000  # You can adjust this value
            damping = 1    # You can adjust this value

            self.joint = pm.DampedSpring(
                a=self.body_a['body'].body, 
                b=self.body_b['body'].body, 
                anchor_a=self.body_a['local_pos'],
                anchor_b=self.body_b['local_pos'],
                rest_length=rest_length,
                stiffness=stiffness,
                damping=damping
                )
            
            Simulation().space.add(self.joint)
            Simulation().delete_object(self)
            ToolManager().clear()
            Singleton._instances.pop(self.__class__, None) 

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

    def draw_spring(self, canvas, x1, y1, x2, y2, coils=10, amplitude=10):
        # get length and direction
        dx = x2 - x1
        dy = y2 - y1
        length = hypot(dx, dy)

        ux = dx / length
        uy = dy / length

        # perpendicular vector
        px = -uy
        py = ux

        points = [(x1, y1)]
        for i in range(1, coils * 2):
            t = i / (coils * 2)
            # point along the line
            bx = x1 + dx * t
            by = y1 + dy * t

            # coil zigzag amplitude
            offset = amplitude * (1 if i % 2 == 0 else -1)
            bx += px * offset
            by += py * offset

            points.append((bx, by))

        points.append((x2, y2))

        flat_points = [coord for p in points for coord in p]
        canvas.create_line(*flat_points, fill="black", width=2)
    
    def delete(self, space: pm.Space):
        # Check if the joint exists in the space
        if self.joint in space.constraints:
            space.remove(self.joint)
            self.joint = None
