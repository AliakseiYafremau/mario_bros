from game.domain.difficulty import selected_difficulty
from game.domain.elements import Element
from game.domain.exceptions import DomainError
from game.domain.difficulty import Difficulty


class Window:
    def __init__(
        self,
        difficulty: Difficulty = Difficulty(0),
        width: int = selected_difficulty.difficulty_values()["window_width"],
        height: int = selected_difficulty.difficulty_values()["window_height"],
    ):
        self.width = width
        self.height = height


running_window = Window()  # Manually altering window resolution is not recommended


class PointsCounter(Element):
    def __init__(self, x: int, y: int, length: int, height: int) -> None:
        super().__init__(x, y, length, height)
        self.digit1_value = 0
        self.digit2_value = 0
        self.digit3_value = 0
        self.digit4_value = 0

    def update_points(self, points: int):
        if len(str(points)) > 4:
            raise DomainError("Thats it, you won, you have more than 9999 points.")
        if len(str(points)) == 4:
            self.digit4_value = int(str(points)[-4])
            self.digit3_value = int(str(points)[-3])
            self.digit2_value = int(str(points)[-2])
            self.digit1_value = int(str(points)[-1])
        elif len(str(points)) == 3:
            self.digit3_value = int(str(points)[-3])
            self.digit2_value = int(str(points)[-2])
            self.digit1_value = int(str(points)[-1])
        elif len(str(points)) == 2:
            self.digit2_value = int(str(points)[-2])
            self.digit1_value = int(str(points)[-1])
        elif len(str(points)) == 1:
            self.digit1_value = int(str(points)[-1])


class LivesCounter(Element):
    def __init__(self, x: int, y: int, length: int, height: int) -> None:
        super().__init__(x, y, length, height)


# FIXME this will make it so that lives are regened
class DeliveriesCounter(Element):
    def __init__(self, x: int, y: int, length: int, height: int) -> None:
        super().__init__(x, y, length, height)


class RenderedElements:
    def __init__(self):
        "TO BE IMPLEMENTED"
