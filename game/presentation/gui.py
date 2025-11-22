from game.domain.difficulty import selected_difficulty
from game.domain.game import Game
from game.presentation.pyxel_elements import BoardedPyxelElement, Frame, PyxelElement


class Window:
    def __init__(self, width: int = 500):
        self.width = selected_difficulty.difficulty_values()["window_width"]
        self.height = selected_difficulty.difficulty_values()["window_height"]


running_window = Window()  # Manually altering window resolution is not recommended


class RenderedElements:

    def __init__(self):
        "TO BE IMPLEMENTED"
