import random


class Difficulty:
    """Difficulty preset selector that exposes derived gameplay constants.

    Attributes:
        difficulty (int): An integer between 0 and 3 representing the difficulty.
    """

    def __init__(self, difficulty: int = 0) -> None:
        """Initializes a new Difficulty instance.

        :param difficulty: int, the difficulty level (0, 1, 2 or 3).
        :raises TypeError: if difficulty is not an int.
        :raises ValueError: if difficulty is not in {0, 1, 2, 3}.
        """
        self.difficulty = difficulty

    @property
    def difficulty(self) -> int:
        """Returns the current difficulty level.

        :return: int, the difficulty level (0, 1, 2 or 3).
        """
        return self.__difficulty

    @difficulty.setter
    def difficulty(self, value: int) -> None:
        """Sets the difficulty level.

        :param value: int, the new difficulty level (0, 1, 2 or 3).
        :raises TypeError: if value is not an int.
        :raises ValueError: if value is not in {0, 1, 2, 3}.
        """
        if not isinstance(value, int):
            raise TypeError("The difficulty must be an int 0, 1, 2, or 3")
        if value not in (0, 1, 2, 3):
            raise ValueError("The difficulty must be 0, 1, 2, or 3")
        self.__difficulty = value

    def difficulty_values(self) -> dict:
        """Returns a dictionary of gameplay constants for the current difficulty.

        This includes the number of belts, conveyor speeds, score increase,
        lives eliminated, window dimensions and whether controls are reversed.

        :return: dict, mapping configuration names to their values for this difficulty.
        """
        BELTS = (5, 7, 9, 5)
        CONVEYOR_SPEED = (
            (0.75, 1, 1),
            (0.75, 1, 1.5),
            (0.75, 1.5, 2),
            (0.75, random.uniform(1, 2), random.uniform(1, 2)),
        )
        INCREASE = (50, 30, 30, 20)
        ELIMINATES = (3, 5, 5, 0)
        WINDOW_HEIGHT = (325, 425, 525, 325)
        WINDOW_WIDTH = (500, 500, 500, 500)
        REVERSED_CONTROLS = self.difficulty == 3

        return {
            "belts": BELTS[self.difficulty],
            "conveyor_speed": CONVEYOR_SPEED[self.difficulty],
            "increase": INCREASE[self.difficulty],
            "eliminates": ELIMINATES[self.difficulty],
            "reversed_controls": REVERSED_CONTROLS,
            "window_height": WINDOW_HEIGHT[self.difficulty],
            "window_width": WINDOW_WIDTH[self.difficulty],
        }
