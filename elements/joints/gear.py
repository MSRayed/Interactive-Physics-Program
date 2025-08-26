import pymunk as pm
from tkinter import PhotoImage
from tkinter.constants import CENTER

from elements.tool import Tool
from simulation import Simulation
from utils import Singleton
from ui.toolManager import ToolManager


class Gear(Tool, metaclass=Singleton):
    NAME: str = "gear"

    def __init__(self, id):
        Tool.__init__(self, id)

        self.ratio = 10.0

        self.joint: pm.Constraint = None

        self.body_a = {
            'body': None, # Body object
            'pos': None, # Body position in world coordinates
            'local_pos': None # Click position in local coordinates
            }
        
        self.body_b = {'body': None, 'pos': None, 'local_pos': None}

        self.mouse_position = None

        self.icon = PhotoImage(
            file="tool_menu_buttons_removed_background_1/gear.png"
            )


    def draw(self, cnv):
        super().draw(cnv)

        body_a, body_b = self.body_a, self.body_b

        if body_b['body'] is None:
            return

        anchor_a = body_a['body'].body.position
        anchor_b = body_b['body'].body.position

        cnv.create_image(anchor_a.x, anchor_a.y, image=self.icon, anchor=CENTER)
        cnv.create_image(anchor_b.x, anchor_b.y, image=self.icon, anchor=CENTER)

        cnv.create_line(
            anchor_a.x, 
            anchor_a.y, 
            anchor_b.x, 
            anchor_b.y, 
            fill="black", 
            width=1
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
            self.position = self.parent.position
            return True

    def initialize(self):
        # if multiple bodies are piled up, select the top one
        if type(self.parent) is list:
            self.parent = self.parent[0]

        body = self.parent

        if not self.body_a['body']:
            self.body_a['body'] = body
            self.body_a['pos'] = body.position

        elif not self.body_b['body']:
            self.body_b['body'] = body
            self.body_b['pos'] = body.position
            
            self.joint = pm.GearJoint(
                self.body_a['body'].body, 
                self.body_b['body'].body,
                phase=0, 
                ratio=self.ratio
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
    
    def delete(self, space: pm.Space):
        # Check if the joint exists in the space
        if self.joint in space.constraints:
            space.remove(self.joint)
            self.joint = None
