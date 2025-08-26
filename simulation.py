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

        self._lock = threading.Lock()

    def start(self):
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._loop, daemon=True)
            self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(0.01)
            self._thread = None

    def reset(self):
        for obj in self.objects:
            obj.reset()
        
        self.step()

    def _loop(self):
        while self._running:
            self.step()

    def step(self):
        start_time = time.perf_counter()

        self.space.step(self.dt)

        with self._lock:
            for obj in self.objects:
                obj.update()

        for callback in self._observers: callback()

        elapsed = time.perf_counter() - start_time
        sleep_time = max(0, self.dt - elapsed)
        time.sleep(sleep_time)

    def register_observer(self, callback: Callable):
        self._observers.append(callback)

    def add_object(self, obj: Tool):
        print("Adding ", obj)
        self.objects.append(obj)
        obj.place(self.space)

    def delete_object(self, obj: Tool):
        print("Deleting ", obj)
        self.objects.remove(obj)
    
    def object_at_pos(self, pos: pm.Vec2d, check_bound = False):
        if not self.objects: return None
        
        inside = []

        for element in reversed(Simulation().objects):
            if check_bound:
                if element.point_inside_bounds(pos):
                    inside.append(element)
            else:
                if element.point_inside_shape(pos): 
                    inside.append(element)
                
        if len(inside) == 0: return None
        
        elif len(inside) == 1: inside = inside[0]

        return inside