import pyxel

from game.domain.difficulty import Difficulty


class DifficultySelectorScreen:
    def __init__(self, app):
        self.app = app
        self.selected_difficulty_value: int | None = None

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        elif pyxel.btnp(pyxel.KEY_1):
            self.selected_difficulty_value = 0
        elif pyxel.btnp(pyxel.KEY_2):
            self.selected_difficulty_value = 1
        elif pyxel.btnp(pyxel.KEY_3):
            self.selected_difficulty_value = 2
        elif pyxel.btnp(pyxel.KEY_4):
            self.selected_difficulty_value = 3
        if self.selected_difficulty_value is not None:
            self.app.change_to_game(self.selected_difficulty_value)

    def draw(self):
        pyxel.cls(0)
        pyxel.text(45, 10, "Mario Bros. --- Game & Watch", 4)
        pyxel.text(20, 40, "Press ESC to quit.", 8)
        pyxel.text(20, 75, "Press 1 to play on EASY difficulty.", 11)
        pyxel.text(20, 100, "Press 2 to play on MEDIUM difficulty.", 11)
        pyxel.text(20, 125, "Press 3 to play on EXTREME difficulty.", 11)
        pyxel.text(20, 150, "Press 4 to play on CRAZY difficulty.", 11)