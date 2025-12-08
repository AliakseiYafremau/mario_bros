from game.domain.elements import Element


class Boss(Element):
    """Boss that appears briefly to penalize mistakes.
    The boss is an element that can appear when a mistake is done.
    It records its entrance time and a flag indicating whether it
    has to leave the scene.

    Attributes:
        x (int): The x-coordinate of the boss. Must be non-negative.
        y (int): The y-coordinate of the boss. Must be non-negative.
        length (int): The width of the boss sprite. Must be positive.
        height (int): The height of the boss sprite. Must be positive.
        comes_in_time (float): Time in seconds when the boss appears.
            Must be a float greater than or equal to 0.
        has_to_leave (bool): True if the boss must leave the scene.
    """

    def __init__(
        self,
        x: int,
        y: int,
        length: int,
        height: int,
        comes_in_time: float = 0.0,
        has_to_leave: bool = False,
    ) -> None:
        """Initializes the boss with its position, size and behavior.

        :param x: int, the x-coordinate of the boss, must be >= 0.
        :param y: int, the y-coordinate of the boss, must be >= 0.
        :param length: int, the width of the boss, must be > 0.
        :param height: int, the height of the boss, must be > 0.
        :param comes_in_time: float, time when the boss appears. Must be >= 0.
        :param has_to_leave: bool, True if the boss must leave the scene.
        :raises TypeError: if any parameter type is incorrect.
        :raises ValueError: if any numeric parameter has an invalid value.
        """
        super().__init__(x, y, length, height)
        self.comes_in_time = comes_in_time
        self.has_to_leave = has_to_leave

    @property
    def comes_in_time(self) -> float:
        """Returns the time when the boss appears.

        :return: float, the time in seconds, always >= 0.
        """
        return self.__comes_in_time

    @comes_in_time.setter
    def comes_in_time(self, comes_in_time: float) -> None:
        """Sets the time when the boss appears.

        :param comes_in_time: float, the time in seconds. Must be >= 0.
        :raises TypeError: if comes_in_time is not a number.
        :raises ValueError: if comes_in_time is negative.
        """
        if not isinstance(comes_in_time, (int, float)):
            raise TypeError("comes_in_time must be a number (int or float)")
        comes_in_time = float(comes_in_time)
        if comes_in_time < 0:
            raise ValueError("comes_in_time must be greater than or equal to 0")
        self.__comes_in_time = comes_in_time

    @property
    def has_to_leave(self) -> bool:
        """Returns whether the boss must leave the scene.

        :return: bool, True if the boss must leave, False otherwise.
        """
        return self.__has_to_leave

    @has_to_leave.setter
    def has_to_leave(self, has_to_leave: bool) -> None:
        """Sets whether the boss must leave the scene.

        :param has_to_leave: bool, True if the boss must leave.
        :raises TypeError: if has_to_leave is not a bool.
        """
        if not isinstance(has_to_leave, bool):
            raise TypeError("has_to_leave must be a bool")
        self.__has_to_leave = has_to_leave