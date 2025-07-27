import tkinter as tk
from tkinter import Tk

from drawingBoard import DrawingBoard

class InteractivePhysics(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.geometry("800x600")
        self.title("Interactive Physics")
        self.mainFrame = tk.Frame(bg="skyblue")
        self.mainFrame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.drawingBoard = DrawingBoard(self.mainFrame)
        self.drawingBoard.pack(padx=5, pady=10, fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    main = InteractivePhysics()
    main.mainloop()