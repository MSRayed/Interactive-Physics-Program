from tkinter import Frame
from utils import Singleton

from ui.toolManager import ToolManager

from typing import List, Optional


class Panel(Frame, metaclass=Singleton):
    def __init__(self, root=None, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.buttons = []
        self.active_index: Optional[int] = None  # None means no selection

    def set_active(self, index: int):
        """Set a button active and reset others."""
        # Clear previous selection
        for btn in self.buttons:
            btn.config(bg=self.cget("bg"))  # reset to default background

        # Set new selection
        self.buttons[index].config(bg="lightblue")
        self.active_index = index
        ToolManager().set_current_tool(self.get_selected_tool())
        ToolManager().set_current_panel(self)
    
    def clear_selection(self):
        """Deselect all buttons."""
        for btn in self.buttons:
            btn.config(bg=self.cget("bg"))
        self.active_index = None
    
    def get_selected_tool(self):
        pass
