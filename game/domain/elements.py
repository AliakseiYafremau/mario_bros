class Element:
    """Base class for all game elements.

    Attributes:
        x (int): The x-coordinate of the element.
        y (int): The y-coordinate of the element.
        length (int): The length of the element.
        height (int): The height of the element.
    """

    def __init__(self, x: int, y: int, length: int, height: int) -> None:
        self.x = x
        self.y = y
        self.length = length
        self.height = height

    def __repr__(self):
        return f"{self.__class__.__name__}(x={self.x}, y={self.y}, length={self.length}, height={self.height})"


class MotionElement(Element):
    """Element that can move in the game.

    Attributes:
        x (int): The x-coordinate of the element.
        y (int): The y-coordinate of the element.
        length (int): The length of the element.
        height (int): The height of the element.
    """

    def move(self, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y

    def move_x(self, x: int) -> None:
        self.move(x=x, y=self.y)

    def move_y(self, y: int) -> None:
        self.move(x=self.x, y=y)
