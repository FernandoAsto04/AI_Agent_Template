from abc import ABC, abstractmethod

class BaseInterface(ABC):
    @abstractmethod
    def start(self, chat):
        pass