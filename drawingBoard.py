from tkinter import Canvas

class DrawingBoard(Canvas):
    def __init__(self, root, *args, **kwargs):
        Canvas.__init__(self, root, *args, **kwargs)

        self.bind("<Button-1>", self.leftClick)
        self.bind("<B1-Motion>", self.leftMouseMotion)
        self.bind("<ButtonRelease-1>", self.leftMouseRelease)
    
    def leftClick(self, event):
        print("left click")
        
    def leftMouseMotion(self, event):
        print("left mouse motion")

    def leftMouseRelease(self, event):
        print("left mouse release")