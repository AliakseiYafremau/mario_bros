from pathlib import Path

import pyxel

from game.presentation.controllers import Controller
from game.presentation.pyxel_elements import PyxelElement


class PyxelApp:
    def __init__(self, *elements: PyxelElement, buttons: dict[int, Controller]):
        self.elements = elements
        self.buttons = buttons

        resource_path = Path(__file__).resolve().parents[2] / "assets" / "res.pyxres"

        pyxel.init(418, 173, title="Pyxel APP")
        pyxel.load(str(resource_path))
        pyxel.run(self.update, self.draw)

    def update(self):
        for button in self.buttons:
            if pyxel.btnp(button):
                self.buttons[button].execute()

    def draw(self):
        pyxel.cls(0)
        for element in self.elements:
            element.draw()
