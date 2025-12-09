from time import perf_counter

import pyxel

from game.presentation.screen import Screen


class DifficultySelectorScreen(Screen):
    """Landing screen that handles difficulty selection and transitions.

    This screen shows a menu for selecting a difficulty level and
    plays a confirmation chime before starting the game.
    """

    def __init__(self, app) -> None:
        """Initializes the difficulty selector screen.

        :param app: the root application that manages screen changes.
        """
        super().__init__(app)
        self.selected_difficulty_value: int | None = None
        # Marks when the confirmation sound started playing.
        self.sound_plays_at: float = 0.0

    def update(self) -> None:
        """Updates the screen logic.

        Handles:
          * quitting the application,
          * difficulty selection,
          * waiting for the confirmation chime before starting the game.
        """
        # When a difficulty was selected wait ~1 second for the chime and then start the game.
        if (
            self.selected_difficulty_value is not None
            and self.sound_plays_at + 1 < perf_counter()
        ):
            self.app.change_to_game(self.selected_difficulty_value)

        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        elif pyxel.btnp(pyxel.KEY_1):
            self.selected_difficulty_value = 0
            pyxel.play(0, 6)
        elif pyxel.btnp(pyxel.KEY_2):
            self.selected_difficulty_value = 1
            pyxel.play(0, 6)
        elif pyxel.btnp(pyxel.KEY_3):
            self.selected_difficulty_value = 2
            pyxel.play(0, 6)
        elif pyxel.btnp(pyxel.KEY_4):
            self.selected_difficulty_value = 3
            pyxel.play(0, 6)

        if self.selected_difficulty_value is not None and self.sound_plays_at == 0.0:
            # Record the moment the sound plays so we can delay the transition.
            self.sound_plays_at = perf_counter()

    def draw(self) -> None:
        """Draws the difficulty selector screen."""
        pyxel.cls(0)
        # Display the instructions for quitting and picking a difficulty level.
        pyxel.text(44, 10, "Mario Bros. --- Game & Watch", 4)
        pyxel.text(20, 40, "-> Press ESC to quit.", 8)
        pyxel.text(20, 75, "-> Press 1 to play on EASY difficulty.", 11)
        pyxel.text(20, 100, "-> Press 2 to play on MEDIUM difficulty.", 11)
        pyxel.text(20, 125, "-> Press 3 to play on EXTREME difficulty.", 11)
        pyxel.text(20, 150, "-> Press 4 to play on CRAZY difficulty.", 11)
