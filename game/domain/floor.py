from game.domain.player import Player


class Floor:
    """Stationary platform that optionally has a player.

    A floor is defined by its coordinates and can store a reference
    to a :class:`Player` if it is standing on it.

    Attributes:
        x (int): The x-coordinate of the floor (non-negative).
        y (int): The y-coordinate of the floor (non-negative).
        player (Player | None): The player currently standing on the floor, if any.
    """

    def __init__(self, x: int, y: int, player: Player | None = None) -> None:
        """Initializes a floor with its position and an optional player.

        :param x: int, the x-coordinate of the floor. Must be >= 0.
        :param y: int, the y-coordinate of the floor. Must be >= 0.
        :param player: Player | None, the player standing on this floor, if any.
        :raises TypeError: if x or y are not ints or player has wrong type.
        :raises ValueError: if x or y are negative.
        """
        self.x = x
        self.y = y
        self.player = player

    @property
    def x(self) -> int:
        """Returns the x-coordinate of the floor.

        :return: int, the x-coordinate (non-negative).
        """
        return self.__x

    @x.setter
    def x(self, x: int) -> None:
        """Sets the x-coordinate of the floor.

        :param x: int, the new x-coordinate. Must be >= 0.
        :raises TypeError: if x is not an int.
        :raises ValueError: if x is negative.
        """
        if not isinstance(x, int):
            raise TypeError("Floor x coordinate must be an int")
        if x < 0:
            raise ValueError("Floor x coordinate cannot be negative")
        self.__x = x

    @property
    def y(self) -> int:
        """Returns the y-coordinate of the floor.

        :return: int, the y-coordinate (non-negative).
        """
        return self.__y

    @y.setter
    def y(self, y: int) -> None:
        """Sets the y-coordinate of the floor.

        :param y: int, the new y-coordinate. Must be >= 0.
        :raises TypeError: if y is not an int.
        :raises ValueError: if y is negative.
        """
        if not isinstance(y, int):
            raise TypeError("Floor y coordinate must be an int")
        if y < 0:
            raise ValueError("Floor y coordinate cannot be negative")
        self.__y = y

    @property
    def player(self) -> Player | None:
        """Returns the player standing on this floor, if any.

        :return: Player or None, the player on this floor.
        """
        return self.__player

    @player.setter
    def player(self, player: Player | None) -> None:
        """Sets the player standing on this floor.

        :param player: Player or None, the new player standing on the floor.
        :raises TypeError: if player is not a Player instance or None.
        """
        if player is not None and not isinstance(player, Player):
            raise TypeError("player must be a Player instance or None")
        self.__player = player

    def __eq__(self, value: object) -> bool:
        """Checks equality between floors based on coordinates.

        :param value: object, the other floor to compare with.
        :return: bool, True if both floors have the same x and y.
        """
        if not isinstance(value, Floor):
            return NotImplemented
        return self.x == value.x and self.y == value.y
