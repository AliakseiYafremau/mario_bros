from pdb import run
import pyxel

from game.domain.elements import Element
from game.domain.conveyor import Conveyor
from game.domain.difficulty import selected_difficulty
from game.presentation.gui import running_window, PointsCounter, LivesCounter
from game.domain.floor import Floor
from game.domain.game import Game
from game.domain.package_factory import PackageFactory
from game.domain.player import Player
from game.domain.truck import Truck
from game.presentation.app import PyxelApp
from game.presentation.controllers import MoveDownPlayer, MoveUpPlayer
from game.presentation.pyxel_elements import (
    Frame,
    Grid,
    PyxelElement,
    PyxelStaticElement,
)


def main():
    mario = Player(
        (running_window.width - 96), (running_window.height - 150), 16, 16, "Mario"
    )
    luigi = Player(75, (running_window.height - 150), 16, 16, "Luigi")

    # FIXME some floors(floor 1 for luigi for example) to be removed cause the player will never need to be there
    floors_mario = [
        Floor(x=mario.x, y=(running_window.height - 100 - i * 50), player=None)
        for i in range(selected_difficulty.difficulty_values()["belts"] - 1)
    ]
    floors_luigi = [
        Floor(x=luigi.x, y=(running_window.height - 100 - i * 50), player=None)
        for i in range(selected_difficulty.difficulty_values()["belts"])
    ]
    floors_luigi[1].player = luigi
    floors_mario[1].player = mario
    floors = [floors_luigi, floors_mario]

    speed = selected_difficulty.difficulty_values()["conveyor_speed"]
    conveyors = [
        Conveyor(
            conveyor_id=i + 1,
            x=100,
            y=(running_window.height - 75 - i * 50),
            length=(running_window.width - 200),
            height=8,
            speed=speed,
            finish_floor=floors[i % 2][i],
        )
        for i in range(selected_difficulty.difficulty_values()["belts"])
    ]

    factory_conveyor = Conveyor(
        conveyor_id=0,
        x=running_window.width - 75,
        y=running_window.height - 75,
        length=60,
        height=8,
        speed=speed,
        finish_floor=floors_mario[0],
    )

    truck = Truck(
        x=conveyors[-1].x - 80,
        y=conveyors[-1].y - 30,
        length=45,
        height=30,
    )

    point_counter_background = Element(
        x=running_window.width - 75, y=17, length=47, height=17
    )
    point_counter = PointsCounter(
        x=(point_counter_background.x + 4), y=20, length=39, height=11
    )
    lives_counter = LivesCounter(
        x=point_counter_background.x + (point_counter_background.length - 32),
        y=(point_counter_background.y + point_counter_background.height),
        length=32,
        height=21,
    )

    for i in range(selected_difficulty.difficulty_values()["belts"]):
        if i != (selected_difficulty.difficulty_values()["belts"] - 1):
            conveyors[i].next_step = conveyors[i + 1]
        else:
            conveyors[i].next_step = truck
    factory_conveyor.next_step = conveyors[0]

    package_factory = PackageFactory(
        running_window.width - 115 + factory_conveyor.length - 20,
        running_window.height - 110,
        60,
        40,
        12,
        8,
        conveyor=factory_conveyor,
    )

    game = Game(
        players={
            mario: floors_mario,
            luigi: floors_luigi,
        },
        conveyors=[factory_conveyor, *conveyors],
        factories=[package_factory],
        truck=truck,
        point_counter=point_counter,
    )

    move_up_mario = MoveUpPlayer(
        game=game,
        player=mario,
    )
    move_down_mario = MoveDownPlayer(
        game=game,
        player=mario,
    )
    move_up_luigi = MoveUpPlayer(
        game=game,
        player=luigi,
    )
    move_down_luigi = MoveDownPlayer(
        game=game,
        player=luigi,
    )

    conveyor_middle_frames = [Frame(1, 16, 88, 16, 8) for i in range(35)]
    rendered_conveyors = [
        PyxelElement(
            conveyors[i],
            Frame(1, 0, 24, 8, 8),
            *conveyor_middle_frames,
            Frame(1, 0, 32, 16, 8),
            grid=Grid.ROW,
        )
        for i in range(selected_difficulty.difficulty_values()["belts"])
    ]
    # Static elements
    conveyor_transformers_frames = [
        Frame(1, 32, 16 + i * 16, 16, 16, scale=2)
        for i in range(selected_difficulty.difficulty_values()["belts"])
    ]
    static_conveyor_frames = [
        PyxelStaticElement(
            running_window.width // 2,
            (running_window.height - 87 - i * 50),
            conveyor_transformers_frames[i],
        )
        for i in range(selected_difficulty.difficulty_values()["belts"])
    ]
    static_ladders_frames = [
        PyxelStaticElement(
            50,
            (running_window.height - 97 - i * 50),
            Frame(1, 0, 88, 16, 16, scale=2),
        )
        for i in range(selected_difficulty.difficulty_values()["belts"])
    ]
    static_ladders_frames.pop(-1)
    static_ladders_platforms = [
        PyxelStaticElement(
            75,
            (running_window.height - 70 - i * 50),
            Frame(1, 0, 104, 16, 3, scale=2),
        )
        for i in range(selected_difficulty.difficulty_values()["belts"])
    ]
    static_ladders_platforms_for_ladders = [
        PyxelStaticElement(
            50,
            (running_window.height - 70 - i * 50),
            Frame(1, 0, 104, 16, 3, scale=2),
        )
        for i in range(selected_difficulty.difficulty_values()["belts"])
    ]
    static_ladders_platforms_for_ladders.pop(-1)

    PyxelApp(
        *static_conveyor_frames,
        *static_ladders_frames,
        *static_ladders_platforms,
        *static_ladders_platforms_for_ladders,
        (PyxelElement(mario, Frame(0, 16, 0, 16, 16, scale=2))),
        (PyxelElement(luigi, Frame(0, 0, 0, 16, 16, scale=2))),
        (PyxelElement(package_factory, Frame(0, 64, 96, 60, 40))),
        *rendered_conveyors,
        PyxelElement(
            factory_conveyor,
            Frame(1, 0, 24, 8, 8),
            Frame(1, 16, 88, 16, 8),
            Frame(1, 16, 88, 16, 8),
            Frame(1, 16, 88, 16, 8),
            Frame(1, 16, 88, 16, 8),
            Frame(1, 16, 88, 16, 8),
            Frame(1, 0, 32, 16, 8),
            grid=Grid.ROW,
        ),
        PyxelElement(truck, Frame(0, 131, 1, 45, 30)),
        PyxelElement(point_counter_background, Frame(0, 96, 144, 47, 17)),
        PyxelElement(
            point_counter,
            Frame(0, 53, 18, 6, 11, 11),
            Frame(0, 53, 18, 6, 11, 11),
            Frame(0, 53, 18, 6, 11, 11),
            Frame(0, 53, 18, 6, 11, 11),
            grid=Grid.ROW,
        ),
        PyxelElement(lives_counter, Frame(0, 64, 139, 32, 21)),
        buttons={
            pyxel.KEY_UP: move_up_mario
            if not selected_difficulty.difficulty_values()["reversed_controls"]
            else move_down_mario,
            pyxel.KEY_DOWN: move_down_mario
            if not selected_difficulty.difficulty_values()["reversed_controls"]
            else move_up_mario,
            pyxel.KEY_W: move_up_luigi
            if not selected_difficulty.difficulty_values()["reversed_controls"]
            else move_down_luigi,
            pyxel.KEY_S: move_down_luigi
            if not selected_difficulty.difficulty_values()["reversed_controls"]
            else move_up_luigi,
        },
        game=game,
        tick_second=1,
        move_truck_tick=0.07,
        move_package_tick=0.15,
        create_package_tick=5,
    )


if __name__ == "__main__":
    main()
