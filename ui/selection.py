from tkinter import Canvas

from elements.tool import Tool

class Selection:
    def __init__(self, cnv: Canvas):
        self.cnv = cnv
    
    def highlight(self, curr):
        self.curr = curr

        for x in [curr.left, curr.right]:
            for y in [curr.top, curr.bottom]:
                self.draw_corner(x, y)
    
    def draw_corner(self, x, y):
        self.cnv.create_rectangle(x-Tool.cornerSize, y-Tool.cornerSize, x+Tool.cornerSize, y+Tool.cornerSize, fill="black")

