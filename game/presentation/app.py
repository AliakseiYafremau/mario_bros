from pathlib import Path
from time import perf_counter

import pyxel

from game.domain.game import Game
from game.presentation.gui import Window
from game.presentation.controllers import Controller
from game.presentation.pyxel_elements import BoardedPyxelElement, Frame, PyxelElement


class PyxelApp:
    def __init__(
        self,
        *elements: PyxelElement,
        buttons: dict[int, Controller],
        game: Game,
        tick_second: float,
        move_package_tick: int,
        create_package_tick: int,
    ):
        self.elements = list(elements)
        self.buttons = buttons
        self.game = game
        self.tick_second = tick_second
        self.move_package_tick = move_package_tick
        self.create_package_tick = create_package_tick
        self._last_create_package_time = perf_counter()
        self._last_move_package_time = perf_counter()
        running_window = Window()

        resource_path = (
            Path(__file__).resolve().parents[2] / "assets" / "global_sprites.pyxres"
        )
        pyxel.init(running_window.width, running_window.height, title="Pyxel APP", fps=60, quit_key=pyxel.KEY_ESCAPE)
        pyxel.load(str(resource_path))
        pyxel.run(self.update, self.draw)

    def update(self):
        for button in self.buttons:
            if pyxel.btnp(button):
                self.buttons[button].execute()

        for new_package in self.game.newly_created_packages:
            self.elements.append(
                BoardedPyxelElement(PyxelElement(new_package, Frame(0, 66, 67, 11, 7)))
            )
            self.game.newly_created_packages.remove(new_package)

        current_time = perf_counter()
        if (
            current_time - self._last_move_package_time
            >= self.tick_second * self.move_package_tick
        ):
            self._last_move_package_time = current_time
            self.game.move_packages()

        if (
            current_time - self._last_create_package_time
            >= self.tick_second * self.create_package_tick
        ):
            self._last_create_package_time = current_time
            self.game.create_package()

    def draw(self):
        pyxel.cls(0)
        for element in self.elements:
            element.draw()
