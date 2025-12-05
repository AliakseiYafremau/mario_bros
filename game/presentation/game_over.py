import pyxel

from game.presentation.screen import Screen
from game.presentation.main_app import App


class GameOverScreen(Screen):
    def __init__(self, app: App):
        super().__init__(app)
        self.wants_to_retry: bool = False

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        elif pyxel.btnp(pyxel.KEY_DELETE):
            self.wants_to_retry = True

    def draw(self):
        pyxel.cls(0)
        pyxel.text(20, 25, "YOU LOSE. You ran out of lives.", 7)
        pyxel.text(20, 75, "Press ESC to quit.", 7)
        pyxel.text(20, 100, "Press DELETE to play again.", 7)