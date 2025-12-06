import pyxel

from game.presentation.screen import Screen


class GameOverScreen(Screen):
    def __init__(self, app):
        super().__init__(app)

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        elif pyxel.btnp(pyxel.KEY_SPACE):
            self.app.change_to_difficulty_selector()

    def draw(self):
        pyxel.cls(0)
        pyxel.text(45, 10, "Mario Bros. --- Game & Watch", 4)
        pyxel.text(45, 30, "YOU LOSE!!! You ran out of lives!", 7)
        pyxel.text(20, 100, "Press ESC to quit.", 8)
        pyxel.text(20, 125, "Press SPACE to play again.", 11)