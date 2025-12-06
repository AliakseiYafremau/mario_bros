import pyxel


class GameOverScreen:
    def __init__(self, app):
        self.app = app

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        elif pyxel.btnp(pyxel.KEY_SPACE):
            self.app.change_to_difficulty_selector()

    def draw(self):
        pyxel.cls(0)
        pyxel.text(20, 25, "YOU LOSE. You ran out of lives.", 7)
        pyxel.text(20, 75, "Press ESC to quit.", 7)
        pyxel.text(20, 100, "Press SPACE to play again.", 7)