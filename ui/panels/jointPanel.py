import math

from .panel import Panel

from elements.joints import PinJoint, Spring, Rope, Gear, RigidJoint

from ui.toolManager import ToolManager

JOINTS = [
    PinJoint, 
    RigidJoint,
    Spring, 
    Rope, 
    Gear, 
    ]


class JointPanel(Panel):
    def __init__(self, root=None, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        
        # Create pin buttons
        for i, joint in enumerate(JOINTS):
            btn = ToolManager().generate_tool_button(self, file=f"tool_menu_buttons_removed_background_1/{joint.NAME}.png", 
                                                    name=joint.NAME, 
                                                    command=lambda idx=i: self.set_active(idx))
            btn.grid(column=i % 2, row=math.ceil((i + 1) / 2))
            self.buttons.append(btn)
    
    def get_selected_tool(self):
        """Return the currently selected shape class or None."""
        if self.active_index is None or self.active_index >= len(JOINTS):
            return None  # None if nothing or anchor is selected
        return JOINTS[self.active_index]