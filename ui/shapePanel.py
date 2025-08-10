import math
from tkinter import Frame, PhotoImage, Button
from elements import Rectangle, Circle, Shape
from typing import List, Optional

SHAPES: List[Shape] = [Rectangle, Circle]


class ShapePanel(Frame):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, root=None, *args, **kwargs):
        if hasattr(self, '_initialized') and self._initialized:
            return

        super().__init__(root, *args, **kwargs)

        self.images = []
        self.buttons = []
        self.active_index: Optional[int] = None  # None means no selection

        # Create shape buttons
        for i, shape in enumerate(SHAPES):
            img = PhotoImage(file=f"tool_menu_buttons_removed_background_1/{shape.NAME}.png")
            self.images.append(img)
            btn = Button(
                self, image=img, text=shape.NAME, borderwidth=0,
                command=lambda idx=i: self.set_active(idx)
            )
            btn.grid(column=i % 2, row=math.ceil((i + 1) / 2))
            self.buttons.append(btn)

        # Anchor button
        anchor_img = PhotoImage(file=f"tool_menu_buttons_removed_background_1/anchor.png")
        self.images.append(anchor_img)
        anchor_index = len(SHAPES)
        btn_anchor = Button(
            self, image=anchor_img, text="Anchor", borderwidth=0,
            command=lambda idx=anchor_index: self.set_active(idx)
        )
        btn_anchor.grid(column=anchor_index % 2, row=math.ceil((anchor_index + 1) / 2))
        self.buttons.append(btn_anchor)

        self._initialized = True

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
