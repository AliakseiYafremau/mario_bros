class Element:
    """Base class for all game elements.

    This class represents any element that has a position and a size
    in the game world.

    Attributes:
        x (int): The x-coordinate of the element. It must be a non-negative integer.
        y (int): The y-coordinate of the element. It must be a non-negative integer.
        length (int): The length (width) of the element. It must be a positive integer.
        height (int): The height of the element. It must be a positive integer.
    """

    def __init__(self, x: int, y: int, length: int, height: int) -> None:
        """Initializes the element with its position and size.

        :param x: int, the x-coordinate of the element. Must be >= 0.
        :param y: int, the y-coordinate of the element. Must be >= 0.
        :param length: int, the length (width) of the element. Must be > 0.
        :param height: int, the height of the element. Must be > 0.
        :raises TypeError: if any parameter is not an int.
        :raises ValueError: if any coordinate is negative or any dimension is not positive.
        """
        self.x = x
        self.y = y
        self.length = length
        self.height = height

    def __repr__(self) -> str:
        """Returns a string representation of the element.

        :return: str, a representation including the class name and its attributes.
        """
        return (
            f"{self.__class__.__name__}(x={self.x}, "
            f"y={self.y}, length={self.length}, height={self.height})"
        )

    # x property
    @property
    def x(self) -> int:
        """Returns the x-coordinate of the element.

        :return: int, the x-coordinate (non-negative).
        """
        return self.__x

    @x.setter
    def x(self, x: int) -> None:
        """Sets the x-coordinate of the element.

        :param x: int, the new x-coordinate. Must be a non-negative integer.
        :raises TypeError: if x is not an int.
        """
        if not isinstance(x, int):
            raise TypeError("The x coordinate must be an int")
        self.__x = x

    # y property
    @property
    def y(self) -> int:
        """Returns the y-coordinate of the element.

        :return: int, the y-coordinate (non-negative).
        """
        return self.__y

    @y.setter
    def y(self, y: int) -> None:
        """Sets the y-coordinate of the element.

        :param y: int, the new y-coordinate. Must be a non-negative integer.
        :raises TypeError: if y is not an int.
        :raises ValueError: if y is negative.
        """
        if not isinstance(y, int):
            raise TypeError("The y coordinate must be an int")
        if y < 0:
            raise ValueError("The y coordinate cannot be negative")
        self.__y = y

    # length property
    @property
    def length(self) -> int:
        """Returns the length (width) of the element.

        :return: int, the length (must be positive).
        """
        return self.__length

    @length.setter
    def length(self, length: int) -> None:
        """Sets the length (width) of the element.

        :param length: int, the new length. Must be a positive integer.
        :raises TypeError: if length is not an int.
        :raises ValueError: if length is not positive.
        """
        if not isinstance(length, int):
            raise TypeError("The length must be an int")
        if length < 0:
            raise ValueError("The length must be a positive integer or 0")
        self.__length = length

    # height property
    @property
    def height(self) -> int:
        """Returns the height of the element.

        :return: int, the height (must be positive).
        """
        return self.__height

    @height.setter
    def height(self, height: int) -> None:
        """Sets the height of the element.

        :param height: int, the new height. Must be a positive integer.
        :raises TypeError: if height is not an int.
        :raises ValueError: if height is not positive.
        """
        if not isinstance(height, int):
            raise TypeError("The height must be an int")
        if height < 0:
            raise ValueError("The height must be a positive integer or 0")
        self.__height = height


class MotionElement(Element):
    """Element that can move in the game.

    This subclass of :class:`Element` adds movement methods that change
    the position of the element.

    Attributes:
        x (int): The x-coordinate of the element (non-negative).
        y (int): The y-coordinate of the element (non-negative).
        length (int): The length (width) of the element (positive).
        height (int): The height of the element (positive).
    """

    def move(self, x: int = 0, y: int = 0) -> None:
        """Moves the element to a new position.

        :param x: int, the new x-coordinate, must be >= 0.
        :param y: int, the new y-coordinate, must be >= 0.
        :raises TypeError: if x or y are not ints.
        :raises ValueError: if y is negative.
        """
        self.x = int(x)
        self.y = int(y)

    def move_x(self, x: int) -> None:
        """Moves the element horizontally, keeping the y-coordinate.

        :param x: int, the new x-coordinate, must be >= 0.
        :raises TypeError: if x is not an int.
        """
        self.move(x=x, y=self.y)

    def move_y(self, y: int) -> None:
        """Moves the element vertically, keeping the x-coordinate.

        :param y: int, the new y-coordinate, must be >= 0.
        :raises TypeError: if y is not an int.
        :raises ValueError: if y is negative.
        """
        self.move(x=self.x, y=y)
