from game.domain.elements import Element
from game.domain.boss import Boss


class Door(Element):
    """Doorway that controls when the `Boss` sprite enters the scene.

    Attributes:
        x (int): The x-coordinate of the door (non-negative).
        y (int): The y-coordinate of the door (non-negative).
        length (int): The width of the door (positive).
        height (int): The height of the door (positive).
        boss (Boss): The boss that uses this door to enter the scene.
    """

    def __init__(
        self,
        x: int,
        y: int,
        length: int,
        height: int,
        boss: Boss,
    ) -> None:
        """Initializes the door and associates it with a boss.

        :param x: int, the x-coordinate of the door. Must be >= 0.
        :param y: int, the y-coordinate of the door. Must be >= 0.
        :param length: int, the width of the door. Must be > 0.
        :param height: int, the height of the door. Must be > 0.
        :param boss: Boss, the boss associated with this door.
        :raises TypeError: if boss is not a Boss instance.
        :raises TypeError: or ValueError if x, y, length or height are invalid (from Element).
        """
        super().__init__(x, y, length, height)
        self.boss = boss

    @property
    def boss(self) -> Boss:
        """Returns the boss associated with this door.

        :return: Boss, the associated boss instance.
        """
        return self.__boss

    @boss.setter
    def boss(self, boss: Boss) -> None:
        """Sets the boss associated with this door.

        :param boss: Boss, the new boss instance.
        :raises TypeError: if boss is not a Boss instance.
        """
        if not isinstance(boss, Boss):
            raise TypeError("boss must be a Boss instance")
        self.__boss = boss
