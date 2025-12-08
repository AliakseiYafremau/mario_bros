from game.domain.elements import Element
from game.domain.exceptions import DomainError


class PointsCounter(Element):
    """HUD element that tracks and displays a four-digit score."""

    def __init__(self, x: int, y: int, length: int, height: int) -> None:
        super().__init__(x, y, length, height)
        self.digit1_value = 0
        self.digit2_value = 0
        self.digit3_value = 0
        self.digit4_value = 0

    def update_points(self, points: int):
        """Cache each digit of the score for rendering."""
        if len(str(points)) > 4:
            raise DomainError("Thats it, you won, you have more than 9999 points.")
        if len(str(points)) == 4:
            self.digit4_value = int(str(points)[-4])
            self.digit3_value = int(str(points)[-3])
            self.digit2_value = int(str(points)[-2])
            self.digit1_value = int(str(points)[-1])
        elif len(str(points)) == 3:
            self.digit3_value = int(str(points)[-3])
            self.digit2_value = int(str(points)[-2])
            self.digit1_value = int(str(points)[-1])
        elif len(str(points)) == 2:
            self.digit2_value = int(str(points)[-2])
            self.digit1_value = int(str(points)[-1])
        elif len(str(points)) == 1:
            self.digit1_value = int(str(points)[-1])


class LivesCounter(Element):
    """HUD element that anchors the lives indicator sprites."""

    def __init__(self, x: int, y: int, length: int, height: int) -> None:
        super().__init__(x, y, length, height)


# FIXME this will make it so that lives are regened
class DeliveriesCounter(Element):
    """HUD element that anchors the delivered-packages counter."""

    def __init__(self, x: int, y: int, length: int, height: int) -> None:
        super().__init__(x, y, length, height)
