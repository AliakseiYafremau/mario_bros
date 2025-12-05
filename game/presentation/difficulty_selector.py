import pyxel

from game.domain.difficulty import Difficulty


class DifficultySelectorScreen:
    def __init__(self, app):
        self.app = app
        self.selected_difficulty: Difficulty | None = None
        self.has_been_selected: bool = False

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        elif pyxel.btnp(pyxel.KEY_1):
            self.selected_difficulty = Difficulty(0)
            self.has_been_selected = True
        elif pyxel.btnp(pyxel.KEY_2):
            self.selected_difficulty = Difficulty(1)
            self.has_been_selected = True
        elif pyxel.btnp(pyxel.KEY_3):
            self.selected_difficulty = Difficulty(2)
            self.has_been_selected = True
        elif pyxel.btnp(pyxel.KEY_4):
            self.selected_difficulty = Difficulty(3)
            self.has_been_selected = True
        if self.has_been_selected:
            self.app.change_to_game(self.selected_difficulty)

    def draw(self):
        pyxel.cls(0)
        pyxel.text(20, 25, "Press ESC to quit.", 7)
        pyxel.text(20, 50, "Press 1 to play on Easy difficulty.", 7)
        pyxel.text(20, 75, "Press 2 to play on MEDIUM difficulty.", 7)
        pyxel.text(20, 100, "Press 3 to play on EXTREME difficulty.", 7)
        pyxel.text(20, 125, "Press 4 to play on CRAZY difficulty.", 7)