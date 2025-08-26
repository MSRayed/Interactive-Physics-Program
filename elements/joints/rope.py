import pymunk as pm
from tkinter import PhotoImage

from elements.tool import Tool
from simulation import Simulation
from utils import Singleton, polar_to_cartesian
from ui.toolManager import ToolManager


class Rope(Tool, metaclass=Singleton):
    NAME: str = "rope"

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
            file="tool_menu_buttons_removed_background_1/rope.png"
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

        self.draw_rope(
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
            
            max_dist = (
                self.body_a['pos'] 
                + self.body_a['local_pos'] 
                - self.body_b['pos'] 
                - self.body_b['local_pos']
                ).length

            self.joint = pm.SlideJoint(
                a=self.body_a['body'].body, 
                b=self.body_b['body'].body, 
                anchor_a=self.body_a['local_pos'],
                anchor_b=self.body_b['local_pos'],
                min=0,
                max=max_dist
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

    def draw_rope(self, canvas, x1, y1, x2, y2):
        canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
    
    def delete(self, space: pm.Space):
        # Check if the joint exists in the space
        if self.joint in space.constraints:
            space.remove(self.joint)
            self.joint = None
