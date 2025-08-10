from tkinter import Frame, Button, PhotoImage
from simulation import Simulation


class SimulationControlPanel(Frame):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, root=None, *args, **kwargs):
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        super().__init__(root, *args, **kwargs)

        # Load images
        self.runImages = {
            "active": PhotoImage(file="main_menu_removed_background_1/run_active.png"),
            "inactive": PhotoImage(file="main_menu_removed_background_1/run_inactive.png"),
        }

        self.stopImages = {
            "active": PhotoImage(file="main_menu_removed_background_1/stop_active.png"),
            "inactive": PhotoImage(file="main_menu_removed_background_1/stop_inactive.png"),
        }

        self.resetImages = {
            "active": PhotoImage(file="main_menu_removed_background_1/reset_active.png"),
            "inactive": PhotoImage(file="main_menu_removed_background_1/reset_inactive.png"),
        }

        # Simulation reference
        self.simulation = Simulation()

        # Create buttons
        self.runButton = Button(
            self, image=self.runImages["active"],
            command=self.start_simulation, borderwidth=0
        )
        self.stopButton = Button(
            self, image=self.stopImages["inactive"],
            command=self.stop_simulation, borderwidth=0, state="disabled"
        )
        self.resetButton = Button(
            self, image=self.resetImages["inactive"],
            command=self.reset_simulation, borderwidth=0, state="disabled"
        )

        # Pack buttons
        self.runButton.pack(side="left", padx=5)
        self.stopButton.pack(side="left", padx=5)
        self.resetButton.pack(side="left", padx=5)

        self._initialized = True

    def start_simulation(self):
        """Run button pressed."""
        self.simulation.start()
        self.runButton.config(image=self.runImages["inactive"], state="disabled")
        self.stopButton.config(image=self.stopImages["active"], state="normal")
        self.resetButton.config(image=self.resetImages["active"], state="normal")

    def stop_simulation(self):
        """Stop button pressed."""
        self.simulation.stop()
        self.runButton.config(image=self.runImages["active"], state="normal")
        self.stopButton.config(image=self.stopImages["inactive"], state="disabled")
        # Keep reset active even after stopping
        self.resetButton.config(image=self.resetImages["active"], state="normal")

    def reset_simulation(self):
        """Reset button pressed."""
        self.simulation.reset()
