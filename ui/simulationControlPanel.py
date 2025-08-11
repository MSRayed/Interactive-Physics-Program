from tkinter import Frame
from simulation import Simulation
from ui.toolManager import ToolManager

from utils import Singleton


class SimulationControlPanel(Frame, metaclass=Singleton):
    def __init__(self, root=None, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        # Simulation reference
        self.simulation = Simulation()

        self.runButton = ToolManager().generate_tool_button(self, file="main_menu_removed_background_1/run_active.png",
                                                            name="Run", 
                                                            command=self.start_simulation
                                                            )

        self.stopButton = ToolManager().generate_tool_button(self, file="main_menu_removed_background_1/stop_active.png",
                                                            name="Stop", 
                                                            command=self.stop_simulation
                                                            )

        self.resetButton = ToolManager().generate_tool_button(self, file="main_menu_removed_background_1/reset_active.png",
                                                            name="Reset", 
                                                            command=self.reset_simulation
                                                            )
        
        # Stopped at startup
        self.stop_simulation()

        # Pack buttons
        self.runButton.pack(side="left", padx=5)
        self.stopButton.pack(side="left", padx=5)
        self.resetButton.pack(side="left", padx=5)

    def start_simulation(self):
        """Run button pressed."""
        self.simulation.start()
        self.runButton.config( state="disabled")
        self.stopButton.config(state="normal")
        self.resetButton.config( state="normal")

    def stop_simulation(self):
        """Stop button pressed."""
        self.simulation.stop()
        self.runButton.config(state="normal")
        self.stopButton.config(state="disabled")
        # Keep reset active even after stopping
        self.resetButton.config( state="normal")

    def reset_simulation(self):
        """Reset button pressed."""
        self.simulation.reset()
