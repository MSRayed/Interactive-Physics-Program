import pymunk as pm
from typing import List, Callable
from utils import Singleton
from elements.tool import Tool

import threading
import time


class Simulation(metaclass=Singleton):
    objects: List[Tool] = []
    def __init__(self):
        self.space = pm.Space()
        self.space.gravity = (0, 981)

        self.framerate = 60
        self.dt = 1.0 / self.framerate
        self._observers: List[Callable] = []

        self._running = False
        self._physicsRunning = False
        self._thread: threading.Thread = None

    def start(self):
        """Start the simulation in a background thread."""
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._loop, daemon=True)
            self._thread.start()

    def stop(self):
        """Stop the simulation loop."""
        self._running = False
        if self._thread:
            self._thread.join()
            self._thread = None

    def reset(self):
        """Reset every object back to original state"""
        for obj in self.objects:
            obj.reset()
        
        self.step()

    def _loop(self):
        """Simulation update loop running in background."""
        while self._running:
            self.step()

    def step(self):
        start_time = time.perf_counter()

        self.space.step(self.dt)

        for obj in self.objects:
            obj.update()

        # For other parts using the clock
        for callback in self._observers:
            callback()

        elapsed = time.perf_counter() - start_time
        sleep_time = max(0, self.dt - elapsed)
        time.sleep(sleep_time)

    def register_observer(self, callback: Callable):
        self._observers.append(callback)

    def add_object(self, obj: Tool):
        self.objects.append(obj)
        obj.place(self.space)
    
    def object_at_pos(self, pos: pm.Vec2d, type = None):
        for element in reversed(Simulation().objects):
            if element.point_inside(pos):
                if type:
                    if isinstance(element, type): return element
                else:
                    return element

    
