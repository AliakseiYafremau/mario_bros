class Element:
    def __init__(self, x: int, y: int, length: int, height: int) -> None:
        self.x = x
        self.y = y
        self.length = length
        self.height = height

    def is_touched(self, element: 'Element') -> bool:
        if not isinstance(element, Element):
            raise TypeError("element must be an Element instance")

        self_left = self.x
        self_right = self.x + self.length
        self_bottom = self.y
        self_top = self.y + self.height

        other_left = element.x
        other_right = element.x + element.length
        other_bottom = element.y
        other_top = element.y + element.height

        is_separated_horizontally = self_right < other_left or other_right < self_left
        is_separated_vertically = self_top < other_bottom or other_top < self_bottom

        return not (is_separated_horizontally or is_separated_vertically)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(x={self.x}, y={self.y}, length={self.length}, height={self.height})"
        )


class MotionElement(Element):
    def move(self, dx: int = 0, dy: int = 0) -> None:
        self.x = self.x + dx
        self.y = self.y + dy

    def move_x(self, dx: int) -> None:
        self.move(dx=dx, dy=0)

    def move_y(self, dy: int) -> None:
        self.move(dx=0, dy=dy)
