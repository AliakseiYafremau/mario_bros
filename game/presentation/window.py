from game.domain.difficulty import Difficulty


class Window:
    def __init__(
            self,
            difficulty: Difficulty | None = None,
            width: int = 0,
            height: int = 0,
    ):
        if difficulty is None:
            self.width = width
            self.height = height
        else:
            self.width = difficulty.difficulty_values()["window_width"]
            self.height = difficulty.difficulty_values()["window_height"]
