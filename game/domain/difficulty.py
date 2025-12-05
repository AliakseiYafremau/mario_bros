import random


class Difficulty:
    def __init__(self, difficulty: int = 0):
        self.difficulty = difficulty

    @property
    def difficulty(self):
        return self.__difficulty

    @difficulty.setter
    def difficulty(self, value):
        if isinstance(value, int):
            self.__difficulty = value
        else:
            raise TypeError("The difficulty must be an int 0, 1, 2, or 3")

    def difficulty_values(self):
        BELTS = (5, 7, 9, 5)
        CONVEYOR_SPEED = (
            (1, 1, 1),
            (1, 1, 1.5),
            (1, 1.5, 2),
            (1, random.uniform(1, 2), random.uniform(1, 2)),
        )
        INCREASE = (50, 30, 30, 20)
        ELIMINATES = (3, 5, 5, 0)
        WINDOW_HEIGHT = (325, 425, 525, 325)
        WINDOW_WIDTH = (500, 500, 500, 500)

        if self.difficulty == 3:
            reversed_controls = True
        else:
            reversed_controls = False
        return {
            "belts": BELTS[self.difficulty],
            "conveyor_speed": CONVEYOR_SPEED[self.difficulty],
            "increase": INCREASE[self.difficulty],
            "eliminates": ELIMINATES[self.difficulty],
            "reversed_controls": reversed_controls,
            "window_height": WINDOW_HEIGHT[self.difficulty],
            "window_width": WINDOW_WIDTH[self.difficulty],
        }