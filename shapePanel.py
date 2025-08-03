from tkinter import Frame, PhotoImage, Radiobutton, IntVar
from elements.shape import Rectangle, Circle, Shape

from typing import List

SHAPES : List[Shape] = [Rectangle, Circle]


class ShapePanel(Frame):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If no instance exists, create a new one
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, root=None, *args, **kwargs):
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        super().__init__(root, *args, **kwargs)

        self.images = []
        self._selectedShape_var = IntVar(self, 0)

        for i, shape in enumerate(SHAPES):
            img = PhotoImage(file=f"tool_menu_buttons_removed_background_1/{shape.NAME}.png")
            self.images.append(img)
            Radiobutton(
                self, value=i, indicator=0, text=shape.NAME, variable=self._selectedShape_var,
                image=img
            ).pack()
        
        self._initialized = True
    
    @property
    def selectedShape(self):
        return SHAPES[self._selectedShape_var.get()]