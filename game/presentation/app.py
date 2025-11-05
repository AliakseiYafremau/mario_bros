from pathlib import Path

import pyxel

from game.presentation.pyxel_elements import PyxelElement


class PyxelApp:
    def __init__(self, *elements: PyxelElement):
        self.elements = elements
        pyxel.init(418, 173, title="Pyxel APP")
        resource_path = Path(__file__).resolve().parents[2] / "assets" / "res.pyxres"
        pyxel.load(str(resource_path))
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        for element in self.elements:
            element.draw()
