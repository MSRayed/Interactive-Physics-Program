from collections.abc import Callable

from tkinter import PhotoImage, Button

from utils import Singleton


class ToolManager(metaclass=Singleton):
    def __init__(self):
        self.imageCache = []
    
    def generate_tool_button(self, root, file, name, command: Callable):
        img = PhotoImage(file=file)
        self.imageCache.append(img)

        btn = Button(root, image=img, text=name, borderwidth=0, command=command)

        return btn

