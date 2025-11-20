from pathlib import Path
from time import perf_counter

import pyxel

from game.domain.game import Game
from game.presentation.gui import running_window
from game.domain.difficulty import selected_difficulty
from game.presentation.controllers import Controller
from game.presentation.pyxel_elements import BoardedPyxelElement, Frame, PyxelElement


class PyxelApp:
    def __init__(
        self,
        *elements: PyxelElement,
        buttons: dict[int, Controller],
        game: Game,
        tick_second: float,
        move_package_tick: float,
        create_package_tick: float,
    ):
        self.elements = list(elements)
        self.buttons = buttons
        self.game = game
        self.tick_second = tick_second
        self.move_package_tick = move_package_tick
        self.create_package_tick = create_package_tick
        self._last_create_package_time = perf_counter()
        self._last_move_package_time = perf_counter()

        resource_path = (
            Path(__file__).resolve().parents[2] / "assets" / "global_sprites.pyxres"
        )
        pyxel.init(running_window.width, running_window.height, title="Pyxel APP", fps=60, quit_key=pyxel.KEY_ESCAPE)
        pyxel.load(str(resource_path))
        pyxel.run(self.update, self.draw)

    def update(self):

        if self.game.points % (selected_difficulty.difficulty_values()["increase"]) == 0:
            self.game.minimum_number_packages = 1 + self.game.points // (selected_difficulty.difficulty_values()["increase"])

        if selected_difficulty.difficulty_values()["eliminates"] != 0 and (
                self.game.stored_deliveries >= selected_difficulty.difficulty_values()["eliminates"]) and (
                self.game.stored_deliveries % selected_difficulty.difficulty_values()["eliminates"] == 0) and (
                self.game.live_amount < 3):
            self.game.live_amount += 1
            self.game.stored_deliveries -= selected_difficulty.difficulty_values()["eliminates"]

        for button in self.buttons:
            if pyxel.btnp(button):
                self.buttons[button].execute()

        for new_package in self.game.newly_created_packages:
            self.elements.append(
                BoardedPyxelElement(PyxelElement(new_package, Frame(0, 66, 67, 11, 7)))
            )
            self.game.newly_created_packages.remove(new_package)
            self.game.packages_at_play += 1

        current_time = perf_counter()
        if (
            current_time - self._last_move_package_time
            >= self.tick_second * self.move_package_tick
        ):
            self._last_move_package_time = current_time
            self.game.move_packages()

        if self.game.packages_at_play < self.game.minimum_number_packages + 1 and (
        current_time - self._last_create_package_time >= self.tick_second * self.create_package_tick):
            self._last_create_package_time = current_time
            self.game.create_package()
            self.create_package_tick = 15

    def draw(self):
        pyxel.cls(0)
        for element in self.elements:
            element.draw()
