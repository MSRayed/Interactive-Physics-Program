from abc import ABC, abstractmethod

class Tool(ABC):
    @staticmethod
    @abstractmethod
    def act(*args, **kwargs):
        pass