from time import perf_counter

import pyxel

from game.presentation.screen import Screen
from game.domain.game import Game
from game.domain.package import Package, PackageState
from game.presentation.gui import PointsCounter, LivesCounter, DeliveriesCounter, Window
from game.domain.difficulty import Difficulty
from game.presentation.controllers import Controller
from game.presentation.pyxel_elements import (
    Frame,
    PyxelElement
)
from game.domain.truck import Truck
from game.domain.elements import Element
from game.domain.player import Player
from game.domain.door import Door
from game.domain.boss import Boss


class GameApp(Screen):
    def __init__(
            self,
            *elements: PyxelElement,
            buttons: dict[int, Controller],
            game: Game,
            tick_second: float,
            move_package_tick: float,
            move_truck_tick: float,
            create_package_tick: float,
            selected_difficulty: Difficulty,
            app
    ):
        self.elements = list(elements)
        self.buttons = buttons
        self.game = game
        self.tick_second = tick_second
        self.move_package_tick = move_package_tick
        self.create_package_tick = create_package_tick
        self.move_truck_tick = move_truck_tick
        self._game_starts_at = perf_counter()
        self._taking_a_break_time = perf_counter()
        self._last_create_package_time = perf_counter()
        self._last_move_package_time = perf_counter()
        self._last_move_truck_time = perf_counter()
        self.selected_difficulty = selected_difficulty
        self.running_window = Window(selected_difficulty)
        super().__init__(app)

        self._fix_eliminates_elements()

    def _fix_eliminates_elements(self):
        for element in self.elements:
            if self.selected_difficulty.difficulty_values()["eliminates"] == 0:
                if (
                        isinstance(element.element, Element)
                        and element.element.x == 428
                        and element.element.y == 45
                ):
                    element.element.length = 41
                    element.element.height = 11
                    element.frames[0].u = 99
                    element.frames[0].v = 195
                    element.frames[0].w = 41
            if self.selected_difficulty.difficulty_values()["eliminates"] == 3:
                if (
                        isinstance(element.element, Element)
                        and element.element.x == 428
                        and element.element.y == 45
                ):
                    element.frames[0].v = 66
            if self.selected_difficulty.difficulty_values()["eliminates"] == 5:
                if (
                        isinstance(element.element, Element)
                        and element.element.x == 428
                        and element.element.y == 45
                ):
                    element.frames[0].v = 98

    def update(self):
        if (
                self.game.points % (self.selected_difficulty.difficulty_values()["increase"])
                == 0
        ):
            self.game.minimum_number_packages = (
                    1
                    + self.game.points
                    // (self.selected_difficulty.difficulty_values()["increase"])
            )

        if (
                self.selected_difficulty.difficulty_values()["eliminates"] != 0
                and (
                self.game.stored_deliveries
                >= self.selected_difficulty.difficulty_values()["eliminates"]
        )
                and (
                self.game.stored_deliveries
                % self.selected_difficulty.difficulty_values()["eliminates"]
                == 0
        )
                and (self.game.live_amount < 3)
        ):
            self.game.live_amount += 1
            self.game.stored_deliveries -= self.selected_difficulty.difficulty_values()[
                "eliminates"
            ]
            self.game.deliveries_to_be_updated = True
            self.game.lives_to_be_updated = True

        if self._taking_a_break_time < perf_counter():
            for button in self.buttons:
                if (
                        pyxel.btnp(button)
                        and not self.buttons[button].player.is_moving_package
                ):
                    self.buttons[button].execute()

        for new_package in self.game.newly_created_packages:
            self.elements.insert(-15, (PyxelElement(new_package, Frame(0, 66, 3, 12, 8, colkey=0))))
            self.game.newly_created_packages.remove(new_package)
            self.game.packages_at_play += 1

        for element in self.elements:
            if (
                    isinstance(element.element, Package)
                    and element.element.stage_to_be_changed_to != 0
            ):
                element.frames[0].v = 3 + (16 * element.element.stage_to_be_changed_to)
                element.element.stage_to_be_changed_to = 0
            if (
                    isinstance(element.element, Package)
                    and element.element.state_to_be_changed_to != 0
            ):
                element.frames[0].u += (element.element.state_to_be_changed_to * 16)
                element.frames[0].h = 10
                element.frames[0].v -= 2
                element.element.state_to_be_changed_to = 0
                self.game.packages_at_play -= 1
                self.game.live_amount -= 1
                self.game.lives_to_be_updated = True
                self.game.boss_comes_in = True
            if isinstance(element.element, Player):
                if self._taking_a_break_time > perf_counter() and not element.element.is_resting:
                    element.frames[0].v = 113
                    element.frames[0].w += 1
                    element.element.is_resting = True
                if element.element.is_resting and self._taking_a_break_time < perf_counter():
                    element.element.is_resting = False
                    element.frames[0].v = 1
                    element.frames[0].w -= 1
                    self.game.boss_comes_in = True
                if element.element.sprite_to_be_changed and not (
                        (element.element.name == "Mario" and element.element.y == self.running_window.height - 100) or (
                        element.element.name == "Luigi" and element.element.y == 25)):
                    element.element.sprite_to_be_changed = False
                    if element.element.package is not None:
                        element.frames[0].v = 17
                    else:
                        element.frames[0].v = 1
                elif element.element.sprite_to_be_changed and (
                        (element.element.name == "Mario" and element.element.y == self.running_window.height - 100) or (
                        element.element.name == "Luigi" and element.element.y == 25)):
                    element.element.sprite_to_be_changed = False
                    element.frames[0].w *= -1
                if element.element.name == "Mario":
                    if element.element.y == self.running_window.height - 100 and not element.element.on_the_factory_level:
                        element.element.on_the_factory_level = True
                        element.frames[0].w += 1
                        element.frames[0].w *= -1
                    if element.element.on_the_factory_level and element.element.y != self.running_window.height - 100:
                        element.element.on_the_factory_level = False
                        element.frames[0].w *= -1
                        element.frames[0].w -= 1
            if isinstance(element.element, Door):
                if self.game.boss_comes_in:
                    if element.frames[0].v != 17:
                        self.elements.append(PyxelElement(element.element.boss, Frame(0, 35, 65, 12, 14, colkey=0, scale=2)))
                        element.frames[0].v = 17
                    element.element.boss.comes_in_time = perf_counter()
                    self.game.boss_comes_in = False
                if element.frames[0].v == 17 and element.element.boss.comes_in_time + 1.5 < perf_counter():
                    element.element.boss.has_to_leave = True
                    element.frames[0].v = 1
            if isinstance(element.element, Boss) and element.element.has_to_leave:
                element.element.has_to_leave = False
                self.elements.remove(element)
            if isinstance(element.element, Package) and element.element.offscreen:
                self.elements.remove(element)

        if self.game.truck.is_full():
            for element in self.elements[:]:
                if (
                        isinstance(element.element, Package)
                        and element.element.state == PackageState.ON_TRUCK
                ) or isinstance(element.element, Truck):
                    self.elements.remove(element)
            self.game.truck.has_returned = False
            self.game.truck.sprite_to_be_changed_back = True
            self.game.truck.packages = []
            self.elements.append(
                (PyxelElement(self.game.truck, Frame(0, 131, 63, 52, 32, colkey=11)))
            )
            self._taking_a_break_time = perf_counter() + 8
            self._last_create_package_time += 8
            self.game.points += 10
            if self.game.stored_deliveries < 9 and self.selected_difficulty.difficulty_values()["eliminates"] != 0:
                self.game.stored_deliveries += 1
                self.game.deliveries_to_be_updated = True
            self.game.points_to_be_updated = True

        if self.game.points_to_be_updated:
            self.game.points_to_be_updated = False
            self.game.point_counter.update_points(self.game.points)
            for element in self.elements:
                if isinstance(element.element, PointsCounter):
                    element.frames[0].v = 18 + 16 * element.element.digit4_value
                    element.frames[1].v = 18 + 16 * element.element.digit3_value
                    element.frames[2].v = 18 + 16 * element.element.digit2_value
                    element.frames[3].v = 18 + 16 * element.element.digit1_value

        if self.game.deliveries_to_be_updated and self.selected_difficulty.difficulty_values()["eliminates"] != 0:
            self.game.deliveries_to_be_updated = False
            for element in self.elements:
                if isinstance(element.element, DeliveriesCounter):
                    element.frames[0].v = 18 + (self.game.stored_deliveries * 16)

        if self.game.lives_to_be_updated:
            self.game.lives_to_be_updated = False
            for element in self.elements:
                if isinstance(element.element, LivesCounter):
                    element.frames[0].v = 144 + 16 * (3 - self.game.live_amount)

        if self.game.live_amount <= 2:
            self.app.change_to_game_over(points=self.game.points, seconds_alive=int(perf_counter()-self._game_starts_at))

        if self._taking_a_break_time < perf_counter():
            for player in self.game.players:
                if (
                        player.is_moving_package
                        and player.package_picked_up_at + self.move_package_tick * 3
                        <= perf_counter()
                ):
                    player.is_moving_package = False
                    player.sprite_to_be_changed = True
                    self.game.player_put_down_package(player)

            current_time = perf_counter()
            if (
                    current_time - self._last_move_package_time
                    >= self.tick_second * self.move_package_tick
            ):
                self._last_move_package_time = current_time
                self.game.move_packages()

            if self.game.first_package_moved and (
                    self.create_package_tick
                    != (self.move_package_tick * 100)
                    * (
                            self.selected_difficulty.difficulty_values()["belts"]
                            / (self.game.minimum_number_packages + 1)
                    )
            ):
                self.create_package_tick = (self.move_package_tick * 100) * (
                        self.selected_difficulty.difficulty_values()["belts"]
                        / (self.game.minimum_number_packages + 1)
                )
            if (
                    self.game.packages_at_play < self.game.minimum_number_packages + 1
                    and (
                            current_time - self._last_create_package_time
                            >= self.tick_second * self.create_package_tick
                    )
            ) or (
                    self.game.packages_at_play < self.game.minimum_number_packages
                    and self.game.first_package_moved
            ):
                self._last_create_package_time = current_time
                self.game.create_package()

        elif (
                perf_counter() - self._last_move_truck_time
                >= self.tick_second * self.move_truck_tick
        ) and not self.game.truck.has_returned:
            self._last_move_truck_time = perf_counter()
            self.game.truck.truck_in_movement(self.game.original_truck_x)
            if self.game.truck.has_turned and self.game.truck.sprite_to_be_changed_back:
                self.game.truck.sprite_to_be_changed_back = False
                for element in self.elements:
                    if isinstance(element.element, Truck):
                        self.elements.remove(element)
                        self.elements.append(
                            (PyxelElement(self.game.truck, Frame(0, 131, 1, 45, 30, colkey=11)))
                        )

    def draw(self):
        pyxel.cls(15)
        for i in range(3):
            pyxel.rect(self.running_window.width - 69 + 16 * i, 0, 4, 30, 1)
        pyxel.rect(0, self.running_window.height - 67, self.running_window.width - 254, 5, 4)
        pyxel.rect(0, 50, 44, self.running_window.height, 4)
        pyxel.rect(0, 50, 100, 13, 4)
        pyxel.rect(0, self.running_window.height - 5, self.running_window.width, 5, 4)
        pyxel.rect(self.running_window.width - 13, 0, 13, self.running_window.height, 4)
        pyxel.rect(self.running_window.width - 150, self.running_window.height - 67, 150, 67, 4)
        pyxel.rect(self.running_window.width - 96, self.running_window.height - 79, 20, 79, 13)
        pyxel.rect(self.running_window.width - 106, self.running_window.height - 65, 40, 67, 13)
        pyxel.rect(self.running_window.width // 2 - 4, 0, 24, self.running_window.height - 62, 13)
        pyxel.rect(self.running_window.width - 50, 96, 39, self.running_window.height - 209, 4)
        for element in self.elements:
            element.draw()
