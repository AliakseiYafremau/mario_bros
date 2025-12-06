from abc import ABC, abstractmethod


class Screen(ABC):
    def __init__(self, app):
        self.app = app

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass
