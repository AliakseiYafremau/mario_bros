import pyxel

from game.presentation.screen import Screen


class GameOverScreen(Screen):
    """Screen shown after the player loses, presenting score, time, and action prompts."""
    def __init__(self, app, points: int, seconds_alive: float):
        self.points = points
        self.seconds_alive = seconds_alive
        super().__init__(app)

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        elif pyxel.btnp(pyxel.KEY_SPACE):
            # Hitting SPACE restarts the flow by returning to the difficulty selector.
            self.app.change_to_difficulty_selector()

    def draw(self):
        pyxel.cls(0)
        # Show loss message plus final score/time so the player can decide to quit or retry.
        pyxel.text(44, 10, "Mario Bros. --- Game & Watch", 4)
        pyxel.text(35, 30, "YOU LOSE!!! You ran out of lives!", 7)
        pyxel.text(20, 80, "-> Press ESC to quit.", 8)
        pyxel.text(20, 105, "-> Press SPACE to play again.", 11)
        pyxel.text(20, 145, "   Your final score was: [" + str(self.points) + "] points!", 10)
        pyxel.text(20, 160, "   You played for: [" + str(self.seconds_alive) + "] seconds!", 10)
