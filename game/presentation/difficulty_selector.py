import pyxel

from game.presentation.screen import Screen
from game.domain.difficulty import Difficulty
from game.presentation.main_app import App


class DifficultySelectorScreen(Screen):
    def __init__(self, app: App):
        super().__init__(app)
        self.selected_difficulty: Difficulty | None = None

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        elif pyxel.btnp(pyxel.KEY_1):
            self.selected_difficulty = Difficulty(0)
        elif pyxel.btnp(pyxel.KEY_2):
            self.selected_difficulty = Difficulty(1)
        elif pyxel.btnp(pyxel.KEY_3):
            self.selected_difficulty = Difficulty(2)
        elif pyxel.btnp(pyxel.KEY_4):
            self.selected_difficulty = Difficulty(3)

    def draw(self):
        pyxel.cls(0)
        pyxel.text(20, 25, "Press ESC to quit.", 7)
        pyxel.text(20, 50, "Press 1 to play on Easy difficulty.", 7)
        pyxel.text(20, 75, "Press 2 to play on MEDIUM difficulty.", 7)
        pyxel.text(20, 100, "Press 3 to play on EXTREME difficulty.", 7)
        pyxel.text(20, 125, "Press 4 to play on CRAZY difficulty.", 7)