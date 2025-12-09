from game.domain.elements import Element
from game.domain.exceptions import DomainError


class PointsCounter(Element):
    """HUD element that tracks and displays a four-digit score.

    Attributes:
        x (int): x-coordinate of the HUD element.
        y (int): y-coordinate of the HUD element.
        length (int): width reserved for rendering.
        height (int): height reserved for rendering.
        digit1_value (int): units digit.
        digit2_value (int): tens digit.
        digit3_value (int): hundreds digit.
        digit4_value (int): thousands digit.
    """

    def __init__(self, x: int, y: int, length: int, height: int) -> None:
        """Initializes the points counter.

        :param x: int, x-coordinate (>= 0).
        :param y: int, y-coordinate (>= 0).
        :param length: int, width of the counter (must be > 0).
        :param height: int, height of the counter (must be > 0).
        """
        super().__init__(x, y, length, height)
        self.digit1_value = 0
        self.digit2_value = 0
        self.digit3_value = 0
        self.digit4_value = 0

    def update_points(self, points: int) -> None:
        """Updates cached digits of the score for rendering.

        :param points: int, the new score [0–9999].
        :raises TypeError: if points is not an int.
        :raises DomainError: if points has more than 4 digits.
        """
        if not isinstance(points, int):
            raise TypeError("points must be an int")

        if points < 0:
            raise DomainError("Points cannot be negative.")
        if len(str(points)) > 4:
            raise DomainError(
                "Thats it, you won, you have more than 9999 points."
            )  # If any player reaches this point might as well force them to stop

        string_points = str(points)

        # Update digits with their respective values
        self.digit1_value = 0
        self.digit2_value = 0
        self.digit3_value = 0
        self.digit4_value = 0

        if len(string_points) >= 1:
            self.digit1_value = int(string_points[-1])
        if len(string_points) >= 2:
            self.digit2_value = int(string_points[-2])
        if len(string_points) >= 3:
            self.digit3_value = int(string_points[-3])
        if len(string_points) == 4:
            self.digit4_value = int(string_points[-4])


class LivesCounter(Element):
    """HUD element that anchors the lives indicator sprites."""

    def __init__(self, x: int, y: int, length: int, height: int) -> None:
        """Initializes the lives counter element.

        :param x: int, x-coordinate.
        :param y: int, y-coordinate.
        :param length: int, width.
        :param height: int, height.
        """
        super().__init__(x, y, length, height)


class DeliveriesCounter(Element):
    """HUD element that anchors the delivered-packages counter."""

    def __init__(self, x: int, y: int, length: int, height: int) -> None:
        """Initializes the deliveries counter element.

        :param x: int, x-coordinate.
        :param y: int, y-coordinate.
        :param length: int, width.
        :param height: int, height.
        """
        super().__init__(x, y, length, height)
