import math
from tkinter import Frame
from elements import Rectangle, Circle, Shape
from typing import List, Optional

from ui.toolManager import ToolManager

from utils import Singleton

SHAPES: List[Shape] = [Rectangle, Circle]


class ShapePanel(Frame, metaclass=Singleton):
    def __init__(self, root=None, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.images = []
        self.buttons = []
        self.active_index: Optional[int] = None  # None means no selection

        # Create shape buttons
        for i, shape in enumerate(SHAPES):
            btn = ToolManager().generate_tool_button(self, file=f"tool_menu_buttons_removed_background_1/{shape.NAME}.png", 
                                                     name=shape.NAME, 
                                                     command=lambda idx=i: self.set_active(idx))
            btn.grid(column=i % 2, row=math.ceil((i + 1) / 2))
            self.buttons.append(btn)

        # Anchor button
        self.anchorButtonIdx = len(SHAPES)

        self.anchorButton = ToolManager().generate_tool_button(self, file="tool_menu_buttons_removed_background_1/anchor.png",
                                                               name="Anchor",
                                                               command=self.set_anchor_active
                                                               )
        self.anchorButton.grid(column=self.anchorButtonIdx % 2, row=math.ceil((self.anchorButtonIdx + 1) / 2))
        self.buttons.append(self.anchorButton)
    
    def set_anchor_active(self):
        self.set_active(self.anchorButtonIdx)

    def set_active(self, index: int):
        """Set a button active and reset others."""
        # Clear previous selection
        for btn in self.buttons:
            btn.config(bg=self.cget("bg"))  # reset to default background

        # Set new selection
        self.buttons[index].config(bg="lightblue")
        self.active_index = index

    def clear_selection(self):
        """Deselect all buttons."""
        for btn in self.buttons:
            btn.config(bg=self.cget("bg"))
        self.active_index = None

    @property
    def selectedShape(self):
        """Return the currently selected shape class or None."""
        if self.active_index is None or self.active_index >= len(SHAPES):
            return None  # None if nothing or anchor is selected
        return SHAPES[self.active_index]
