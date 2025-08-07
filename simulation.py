import pymunk as pm
from typing import List, Callable
from elements import Shape

import threading
import time


class Simulation:
    objects: List[Shape] = []
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return

        self._initialized = True
        self.space = pm.Space()
        self.space.gravity = (0, 981)

        self.framerate = 60
        self.dt = 1.0 / self.framerate
        self._observers: List[Callable] = []

        self._running = False
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

    def _loop(self):
        """Simulation update loop running in background."""
        while self._running:
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

    def add_object(self, obj: Shape):
        self.objects.append(obj)
        obj.place(self.space)
