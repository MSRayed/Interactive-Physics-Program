from collections.abc import Callable

from tkinter import PhotoImage, Button

from utils import Singleton

from elements import Tool


class ToolManager(metaclass=Singleton):
    def __init__(self):
        self.imageCache = []

        self.currentTool: type[Tool] = None 
    
    def generate_tool_button(self, root, file, name, command: Callable):
        img = PhotoImage(file=file)
        self.imageCache.append(img)

        btn = Button(root, image=img, text=name, borderwidth=0, command=command)

        return btn

    def set_current_tool(self, tool: Tool):
        self.currentTool = tool