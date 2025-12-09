import pyxel

from game.presentation.screen import Screen


class GameOverScreen(Screen):
    """Screen shown after the player loses.

    This screen presents the final score, time played and actions to
    either quit or restart.

    Attributes:
        points (int): Final score of the game.
        seconds_alive (float): Time the player survived in seconds.
    """

    def __init__(self, app, points: int, seconds_alive: float) -> None:
        """Initializes the game-over screen.

        :param app: the root application managing screen transitions.
        :param points: int, final score (must be >= 0).
        :param seconds_alive: float, time survived (must be >= 0).
        :raises TypeError: if types are incorrect.
        :raises ValueError: if numeric values are negative.
        """
        self.points = points
        self.seconds_alive = seconds_alive
        super().__init__(app)

    @property
    def points(self) -> int:
        """Returns the final score.

        :return: int, final score (>= 0).
        """
        return self.__points

    @points.setter
    def points(self, points: int) -> None:
        """Sets the final score.

        :param points: int, final score (>= 0).
        :raises TypeError: if points is not an int.
        :raises ValueError: if points is negative.
        """
        if not isinstance(points, int):
            raise TypeError("points must be an int")
        if points < 0:
            raise ValueError("points cannot be negative")
        self.__points = points

    @property
    def seconds_alive(self) -> float:
        """Returns how long the player survived.

        :return: float, time survived in seconds (>= 0).
        """
        return self.__seconds_alive

    @seconds_alive.setter
    def seconds_alive(self, seconds_alive: float) -> None:
        """Sets how long the player survived.

        :param seconds_alive: float, time survived (>= 0).
        :raises TypeError: if seconds_alive is not numeric.
        :raises ValueError: if seconds_alive is negative.
        """
        if not isinstance(seconds_alive, (int, float)):
            raise TypeError("seconds_alive must be a number")
        if seconds_alive < 0:
            raise ValueError("seconds_alive cannot be negative")
        self.__seconds_alive = float(seconds_alive)

    def update(self) -> None:
        """Handles input for quitting or restarting."""
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        elif pyxel.btnp(pyxel.KEY_SPACE):
            # Hitting SPACE restarts the flow by returning to the difficulty selector.
            self.app.change_to_difficulty_selector()

    def draw(self) -> None:
        """Draws the game-over screen."""
        pyxel.cls(0)
        # Show loss message plus final score/time so the player can decide to quit or retry.
        pyxel.text(44, 10, "Mario Bros. --- Game & Watch", 4)
        pyxel.text(35, 30, "YOU LOSE!!! You ran out of lives!", 7)
        pyxel.text(20, 80, "-> Press ESC to quit.", 8)
        pyxel.text(20, 105, "-> Press SPACE to play again.", 11)
        pyxel.text(
            20,
            145,
            f"   Your final score was: [{self.points}] points!",
            10,
        )
        pyxel.text(
            20,
            160,
            f"   You played for: [{self.seconds_alive}] seconds!",
            10,
        )
