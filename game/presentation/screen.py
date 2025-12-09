from abc import ABC, abstractmethod


class Screen(ABC):
    """Abstract Pyxel screen that exposes update/draw hooks.

    A screen is responsible for handling its own logic and drawing.
    It also holds a reference to the root application, which is used
    to change screens (e.g. game, game over, difficulty selection).

    Attributes:
        app: The root application object that manages screen transitions.
    """

    def __init__(self, app) -> None:
        """Initializes the screen with a reference to the application.

        :param app: any object that offers methods to change screens.
        """
        self.app = app

    @abstractmethod
    def update(self) -> None:
        """Advance the screen state for one frame."""
        raise NotImplementedError

    @abstractmethod
    def draw(self) -> None:
        """Render the screen contents."""
        raise NotImplementedError
