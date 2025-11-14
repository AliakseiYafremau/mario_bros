from pathlib import Path
from time import perf_counter

import pyxel

from game.domain.game import Game
from game.presentation.controllers import Controller
from game.presentation.pyxel_elements import PyxelElement


class PyxelApp:
    def __init__(
        self,
        *elements: PyxelElement,
        buttons: dict[int, Controller],
        game: Game,
        tick_second: float,
    ):
        self.elements = elements
        self.buttons = buttons
        self.game = game
        self.tick_second = tick_second
        self._last_tick_time = perf_counter()

        resource_path = (
            Path(__file__).resolve().parents[2] / "assets" / "global_sprites.pyxres"
        )

        pyxel.init(418, 173, title="Pyxel APP")
        pyxel.load(str(resource_path))
        pyxel.run(self.update, self.draw)

    def update(self):
        for button in self.buttons:
            if pyxel.btnp(button):
                self.buttons[button].execute()

        current_time = perf_counter()
        if current_time - self._last_tick_time >= self.tick_second:
            self._last_tick_time = current_time
            self.game.move_packages()

    def draw(self):
        pyxel.cls(0)
        for element in self.elements:
            element.draw()
