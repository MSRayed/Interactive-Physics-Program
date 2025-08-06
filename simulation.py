import pymunk as pm

from typing import List

from elements import Shape


class Simulation:
    objects: List[Shape] = []

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            # If no instance exists, create a new one
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return

        self._initialized = True
    
    def add_object(self, shape: Shape):
        obj = shape(len(self.objects))
        self.objects.append(obj)
        return obj