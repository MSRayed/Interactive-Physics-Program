from abc import abstractmethod

from .tool import Tool
from utils import point_in_circle

from tkinter.constants import CENTER


class ParentedTool(Tool):
    def __init__(self, id):
        Tool.__init__(self, id)
        self.parent = None
        self.icon = None
    
    def draw(self, cnv):
        super().draw(cnv)
        cnv.create_image(self.position.x, self.position.y, image=self.icon, anchor=CENTER)
    
    def initiate(self, event):
        if self.find_parent(event):
            self.position = event
            return True
        return False
    
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

    @abstractmethod
    def find_parent(self, event):
        pass

    @abstractmethod
    def initialize(self):
        pass
    

