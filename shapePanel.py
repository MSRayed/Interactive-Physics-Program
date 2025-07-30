from tkinter import Frame, PhotoImage, Radiobutton, IntVar
from utils import ShapeType


class ShapePanel(Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.circle = PhotoImage(file="tool_menu_buttons_removed_background_1/circle.png")
        self.rectangle = PhotoImage(file="tool_menu_buttons_removed_background_1/rectangle.png")

        self.images = [(self.circle, ShapeType.CIRCLE), (self.rectangle, ShapeType.RECTANGLE)]

        self.selectedShape = IntVar(self, ShapeType.CIRCLE.value)

        for (image, shape) in self.images:
            Radiobutton(self, image=image, value=shape, variable=self.selectedShape, indicator=0,).pack()