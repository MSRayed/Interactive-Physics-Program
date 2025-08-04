from utils import Bound
from elements import Shape


class Circle(Shape):
    NAME = "circle"

    def __init__(self):
        Shape.__init__(self)
        self.fill = "red"
    
    def resize(self, boundX, boundY, newX, newY):
        if boundX == Bound.LEFT:
            anchor_x = self.right
            dx = anchor_x - newX
        elif boundX == Bound.RIGHT:
            anchor_x = self.left
            dx = newX - anchor_x
        else:
            dx = 0

        if boundY == Bound.TOP:
            anchor_y = self.bottom
            dy = anchor_y - newY
        elif boundY == Bound.BOTTOM:
            anchor_y = self.top
            dy = newY - anchor_y
        else:
            dy = 0

        # Choose the smaller of dx and dy to maintain a square
        size = min(abs(dx), abs(dy))

        # Reapply size based on direction of resizing
        if boundX == Bound.LEFT:
            self.left = self.right - size * (1 if dx >= 0 else -1)
        elif boundX == Bound.RIGHT:
            self.right = self.left + size * (1 if dx >= 0 else -1)

        if boundY == Bound.TOP:
            self.top = self.bottom - size * (1 if dy >= 0 else -1)
        elif boundY == Bound.BOTTOM:
            self.bottom = self.top + size * (1 if dy >= 0 else -1)
    

    def draw(self, cnv):
        cnv.create_oval(self.left, 
                        self.top, 
                        self.right, 
                        self.bottom, 
                        fill=None if self.preview else self.fill)