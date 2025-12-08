from abc import ABC, abstractmethod


class Screen(ABC):
    """Abstract Pyxel screen that exposes update/draw hooks."""

    def __init__(self, app):
        self.app = app

    @abstractmethod
    def update(self):
        """Advance the screen state for one frame."""
        pass

    @abstractmethod
    def draw(self):
        """Render the screen contents."""
        pass
