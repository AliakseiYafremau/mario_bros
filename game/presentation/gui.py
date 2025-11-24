from game.domain.difficulty import selected_difficulty
from game.domain.game import Game
from game.domain.elements import Element
from game.presentation.pyxel_elements import BoardedPyxelElement, Frame, PyxelElement


class Window:
    def __init__(self, width: int = 500):
        self.width = selected_difficulty.difficulty_values()["window_width"]
        self.height = selected_difficulty.difficulty_values()["window_height"]


running_window = Window()  # Manually altering window resolution is not recommended

class PointMeter(Element):
    def __init__(self, x: int, y: int, length: int, height: int) -> None:
        super().__init__(x, y, length, height)


class RenderedElements:

    def __init__(self):
        "TO BE IMPLEMENTED"
