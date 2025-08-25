import tkinter as tk
from tkinter import Tk

from ui.drawingBoard import DrawingBoard
from ui.panels.shapePanel import ShapePanel
from ui.panels.jointPanel import JointPanel
from ui.simulationControlPanel import SimulationControlPanel


class InteractivePhysics(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # Windows setup
        self.geometry("800x600")
        self.title("Interactive Physics")

        # Canvas setup
        self.mainFrame = tk.Frame(bg="skyblue")
        self.mainFrame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Tools panel setup
        self.toolsPanel = tk.Frame(self.mainFrame, bg="lightgray")
        self.toolsPanel.pack(side=tk.LEFT, fill=tk.Y)
        
        # Adding canvas functionality
        self.drawingBoard = DrawingBoard(self.mainFrame)
        self.drawingBoard.pack(padx=5, pady=10, fill=tk.BOTH, expand=True)

        # Adding tools to the tools panel
        self.simControlPanel = SimulationControlPanel(self.toolsPanel) 
        self.simControlPanel.pack(padx=20, side=tk.TOP)

        self.shapePanel = ShapePanel(self.toolsPanel)
        self.shapePanel.pack(padx=20, pady=20)

        self.jointPanel = JointPanel(self.toolsPanel)
        self.jointPanel.pack(padx=20, pady=0)



if __name__ == "__main__":
    main = InteractivePhysics()
    main.mainloop()