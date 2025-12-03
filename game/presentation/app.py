from pathlib import Path
from time import perf_counter

import pyxel

from game.domain.game import Game
from game.domain.package import Package, PackageState
from game.presentation.gui import running_window, PointsCounter, LivesCounter, DeliveriesCounter
from game.domain.difficulty import selected_difficulty
from game.presentation.controllers import Controller
from game.presentation.pyxel_elements import (
    Frame,
    PyxelElement,
)
from game.domain.exceptions import DomainError
from game.domain.truck import Truck


class PyxelApp:
    def __init__(
        self,
        *elements: PyxelElement,
        buttons: dict[int, Controller],
        game: Game,
        tick_second: float,
        move_package_tick: float,
        move_truck_tick: float,
        create_package_tick: float,
    ):
        self.elements = list(elements)
        self.buttons = buttons
        self.game = game
        self.tick_second = tick_second
        self.move_package_tick = move_package_tick
        self.create_package_tick = create_package_tick
        self.move_truck_tick = move_truck_tick
        self._taking_a_break = perf_counter()
        self._last_create_package_time = perf_counter()
        self._last_move_package_time = perf_counter()
        self._last_move_truck_time = perf_counter()
        self._took_a_break = False

        resource_path = (
            Path(__file__).resolve().parents[2] / "assets" / "global_sprites.pyxres"
        )
        pyxel.init(
            running_window.width,
            running_window.height,
            title="Pyxel APP",
            fps=60,
            quit_key=pyxel.KEY_ESCAPE,
        )
        pyxel.load(str(resource_path))
        pyxel.run(self.update, self.draw)

    def update(self):
        if (
            self.game.points % (selected_difficulty.difficulty_values()["increase"])
            == 0
        ):
            self.game.minimum_number_packages = (
                1
                + self.game.points
                // (selected_difficulty.difficulty_values()["increase"])
            )

        if (
            selected_difficulty.difficulty_values()["eliminates"] != 0
            and (
                self.game.stored_deliveries
                >= selected_difficulty.difficulty_values()["eliminates"]
            )
            and (
                self.game.stored_deliveries
                % selected_difficulty.difficulty_values()["eliminates"]
                == 0
            )
            and (self.game.live_amount < 3)
        ):
            self.game.live_amount += 1
            self.game.stored_deliveries -= selected_difficulty.difficulty_values()[
                "eliminates"
            ]

        if self._taking_a_break < perf_counter():
            for button in self.buttons:
                if (
                    pyxel.btnp(button)
                    and not self.buttons[button].player.is_moving_package
                ):
                    self.buttons[button].execute()

        for new_package in self.game.newly_created_packages:
            self.elements.append((PyxelElement(new_package, Frame(0, 66, 3, 12, 8, 0))))
            self.game.newly_created_packages.remove(new_package)
            self.game.packages_at_play += 1

        # FIXME optimize this by only changing relevant values
        for element in self.elements:
            if (
                isinstance(element.element, Package)
                and element.element.stage_to_be_changed_to != 0
            ):
                self.elements.append(
                    (
                        PyxelElement(
                            element.element,
                            Frame(
                                element.frames[0].image,
                                element.frames[0].u,
                                3 + (16 * element.element.stage_to_be_changed_to),
                                element.frames[0].w,
                                element.frames[0].h,
                                element.frames[0].colkey,
                            ),
                        )
                    )
                )
                self.elements.remove(element)
                element.element.stage_to_be_changed_to = 0
            if (
                isinstance(element.element, Package)
                and element.element.state_to_be_changed_to != 0
            ):
                self.elements.append(
                    (
                        PyxelElement(
                            element.element,
                            Frame(
                                element.frames[0].image,
                                element.frames[0].u
                                + (element.element.state_to_be_changed_to * 16),
                                element.frames[0].v,
                                element.frames[0].w,
                                element.frames[0].h,
                                element.frames[0].colkey,
                            ),
                        )
                    )
                )
                self.elements.remove(element)
                element.element.state_to_be_changed_to = 0
                self.game.packages_at_play -= 1
                self.game.live_amount -= 1
                self.game.lives_to_be_updated = True
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
                (PyxelElement(self.game.truck, Frame(0, 131, 63, 52, 32)))
            )
            self._taking_a_break = perf_counter() + 8
            self._took_a_break = True
            self.game.points += 10
            if self.game.stored_deliveries < 9:
                self.game.stored_deliveries += 1
                self.game.deliveries_to_be_updated = True
            self.game.points_to_be_updated = True

        if self.game.points_to_be_updated:
            self.game.points_to_be_updated = False
            self.game.point_counter.update_points(self.game.points)
            for element in self.elements:
                if isinstance(element.element, PointsCounter):
                    element.frames[0].v += 16 * element.element.digit4_value
                    element.frames[1].v += 16 * element.element.digit3_value
                    element.frames[2].v += 16 * element.element.digit2_value
                    element.frames[3].v += 16 * element.element.digit1_value

        if self.game.deliveries_to_be_updated:
            self.game.deliveries_to_be_updated = False
            for element in self.elements:
                #FIXME make it so that the hert is its own element
                if isinstance(element.element, LivesCounter):
                    if selected_difficulty.difficulty_values()["eliminates"] == 3:
                        element.frames[0].u = 184
                        element.frames[0].v += 16

        if self.game.lives_to_be_updated:
            self.game.lives_to_be_updated = False
            for element in self.elements:
                if isinstance(element.element, LivesCounter):
                    element.frames[0].v += 16

        if self.game.live_amount <= 0:
            raise DomainError("no more lives left")

        if self._taking_a_break < perf_counter():
            for player in self.game.players:
                if (
                    player.is_moving_package
                    and player.package_picked_up_at + self.move_package_tick * 2
                    <= perf_counter()
                ):
                    player.is_moving_package = False
                    self.game.player_put_down_package(player)

            current_time = perf_counter()
            if (
                current_time - self._last_move_package_time
                >= self.tick_second * self.move_package_tick
            ):
                self._last_move_package_time = current_time
                self.game.move_packages()

            if self._took_a_break:
                self._last_create_package_time += 8
                self._took_a_break = False

            if self.game.first_package_moved and (
                self.create_package_tick
                != (self.move_package_tick * 100)
                * (
                    selected_difficulty.difficulty_values()["belts"]
                    / (self.game.minimum_number_packages + 1)
                )
            ):
                self.create_package_tick = (self.move_package_tick * 100) * (
                    selected_difficulty.difficulty_values()["belts"]
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
                            (PyxelElement(self.game.truck, Frame(0, 131, 1, 45, 30)))
                        )

    def draw(self):
        pyxel.cls(0)
        for element in self.elements:
            element.draw()
