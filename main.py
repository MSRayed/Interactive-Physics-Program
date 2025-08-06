import tkinter as tk
from tkinter import Tk

from ui.drawingBoard import DrawingBoard
from ui.shapePanel import ShapePanel
from simulation import Simulation


class InteractivePhysics(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.geometry("800x600")
        self.title("Interactive Physics")
        self.mainFrame = tk.Frame(bg="skyblue")
        self.mainFrame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.toolsPanel = tk.Frame(self.mainFrame, bg="lightgray")
        self.toolsPanel.pack(side=tk.LEFT, fill=tk.Y)

        self.shapePanel = ShapePanel(self.toolsPanel)
        self.shapePanel.pack(padx=20, pady=20)

        self.drawingBoard = DrawingBoard(self.mainFrame)
        self.drawingBoard.pack(padx=5, pady=10, fill=tk.BOTH, expand=True)

        self.simulation = Simulation()


if __name__ == "__main__":
    main = InteractivePhysics()
    main.mainloop()