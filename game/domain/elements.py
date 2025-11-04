class Element:
    def __init__(self, x: int, y: int, weigth: int, height: int) -> None:
        self.x = x
        self.y = y
        self.weigth = weigth
        self.height = height

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(x={self.x}, y={self.y}, weigth={self.weigth}, height={self.height})"
        )


class MotionElement(Element):
    def move(self, dx: int = 0, dy: int = 0) -> None:
        self.x = self.x + dx
        self.y = self.y + dy

    def move_x(self, dx: int) -> None:
        self.move(dx=dx, dy=0)

    def move_y(self, dy: int) -> None:
        self.move(dx=0, dy=dy)


