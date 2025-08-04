from elements import Shape


class Rectangle(Shape):
    NAME = "rectangle"

    def __init__(self):
        Shape.__init__(self)
        self.fill = "lightgreen"

    def draw(self, cnv):
        cnv.create_rectangle(self.left, 
                            self.top, 
                            self.right, 
                            self.bottom, 
                            fill=None if self.preview else self.fill)