import math
from elements.shapes import Rectangle, Circle, Shape, Anchor
from typing import List

from ui.toolManager import ToolManager

from .panel import Panel

SHAPES: List[Shape] = [Rectangle, Circle]


class ShapePanel(Panel):
    def __init__(self, root=None, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        # Create shape buttons
        for i, shape in enumerate(SHAPES):
            btn = ToolManager().generate_tool_button(self, file=f"tool_menu_buttons_removed_background_1/{shape.NAME}.png", 
                                                    name=shape.NAME, 
                                                    command=lambda idx=i: self.set_active(idx))
            btn.grid(column=i % 2, row=math.ceil((i + 1) / 2))
            self.buttons.append(btn)

        # Anchor button
        anchorButtonIdx = len(SHAPES)

        self.anchorButton = ToolManager().generate_tool_button(self, file="tool_menu_buttons_removed_background_1/anchor.png",
                                                               name="Anchor",
                                                               command=self.set_anchor_active
                                                               )
        self.anchorButton.grid(column=anchorButtonIdx % 2, row=math.ceil((anchorButtonIdx + 1) / 2))
        self.buttons.append(self.anchorButton)
    
    def set_anchor_active(self):
        # Clear previous selection
        for btn in self.buttons:
            btn.config(bg=self.cget("bg"))  # reset to default background

        self.anchorButton.config(bg="lightblue")
        self.active_index = None
        ToolManager().set_current_tool(Anchor)
        ToolManager().set_current_panel(self)

    def get_selected_tool(self):
        """Return the currently selected shape class or None."""
        if self.active_index is None or self.active_index >= len(SHAPES):
            return None  # None if nothing or anchor is selected
        return SHAPES[self.active_index]
