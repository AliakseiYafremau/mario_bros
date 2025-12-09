from game.domain.difficulty import Difficulty


class Window:
    """Centralized holder for Pyxel window dimensions.

    The window can be created either using explicit width and height,
    or by providing a :class:`Difficulty` instance from which the
    dimensions are derived.

    Attributes:
        width (int): Width of the window in pixels, must be > 0.
        height (int): Height of the window in pixels, must be > 0.
    """

    def __init__(
        self,
        difficulty: Difficulty | None = None,
        width: int = 0,
        height: int = 0,
    ) -> None:
        """Initializes the window dimensions.

        :param difficulty: Difficulty | None, if provided, the window size is taken
            from difficulty.difficulty_values()["window_width"] and
            difficulty.difficulty_values()["window_height"].
        :param width: int, explicit window width to use when difficulty is None.
            Must be > 0.
        :param height: int, explicit window height to use when difficulty is None.
            Must be > 0.
        :raises TypeError: if width or height have incorrect type.
        :raises ValueError: if width or height are not positive when used.
        """
        if difficulty is None:
            self.width = width
            self.height = height
        else:
            values = difficulty.difficulty_values()
            self.width = values["window_width"]
            self.height = values["window_height"]

    @property
    def width(self) -> int:
        """Returns the window width.

        :return: int, the width of the window in pixels (> 0).
        """
        return self.__width

    @width.setter
    def width(self, width: int) -> None:
        """Sets the window width.

        :param width: int, the new width in pixels, must be > 0.
        :raises TypeError: if width is not an int.
        :raises ValueError: if width is not positive.
        """
        if not isinstance(width, int):
            raise TypeError("width must be an int")
        if width <= 0:
            raise ValueError("width must be a positive integer")
        self.__width = width

    @property
    def height(self) -> int:
        """Returns the window height.

        :return: int, the height of the window in pixels (> 0).
        """
        return self.__height

    @height.setter
    def height(self, height: int) -> None:
        """Sets the window height.

        :param height: int, the new height in pixels, must be > 0.
        :raises TypeError: if height is not an int.
        :raises ValueError: if height is not positive.
        """
        if not isinstance(height, int):
            raise TypeError("height must be an int")
        if height <= 0:
            raise ValueError("height must be a positive integer")
        self.__height = height
