from utils import Singleton


class ToolManager(metaclass=Singleton):
    def __init__(self):
        self.imageCache = []