from tkinter import *
from tkinter import ttk

class MainWindow():
    def __init__(self):
        self.root = Tk()
        self.frame = ttk.Frame(self.root)

        self.root.title("Interactive Physics")
        self.root.geometry("800x600")
    
    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    main = MainWindow()
    main.start()