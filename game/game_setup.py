import pyxel

from game.domain.elements import Element
from game.domain.conveyor import Conveyor
from game.domain.difficulty import Difficulty
from game.domain.floor import Floor
from game.domain.game import Game
from game.domain.package_factory import PackageFactory
from game.domain.player import Player
from game.domain.truck import Truck
from game.domain.boss import Boss
from game.domain.door import Door
from game.presentation.gui import PointsCounter, LivesCounter, DeliveriesCounter
from game.presentation.window import Window
from game.presentation.game_app import GameApp
from game.presentation.controllers import MoveDownPlayer, MoveUpPlayer
from game.presentation.pyxel_elements import (
    Frame,
    Grid,
    PyxelElement,
    PyxelStaticElement,
)


def create_game_app(selected_difficulty: Difficulty, app) -> GameApp:
    running_window = Window(difficulty=selected_difficulty)
    mario = Player(
        (running_window.width - 96), (running_window.height - 150), 16, 16, "Mario"
    )
    luigi = Player(75, (running_window.height - 150), 16, 16, "Luigi")

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
            floor_y=running_window.height
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
        floor_y=running_window.height
    )

    truck = Truck(
        x=conveyors[-1].x - 80,
        y=conveyors[-1].y - 30,
        length=45,
        height=30,
    )

    point_counter_background = Element(
        x=running_window.width - 75, y=17, length=47, height=21
    )
    point_counter = PointsCounter(
        x=(point_counter_background.x + 4), y=25, length=39, height=11
    )
    deliveries_counter_background = Element(x=point_counter_background.x,
                                            y=(point_counter_background.y + point_counter_background.height) + 4,
                                            length=47,
                                            height=17)
    deliveries_counter = DeliveriesCounter(x=deliveries_counter_background.x + 38,
                                           y=deliveries_counter_background.y + 3,
                                           length=6,
                                           height=11)
    deliveries_counter_hanger = Element(x=deliveries_counter_background.x,
                                        y=deliveries_counter_background.y - 4,
                                        length=47,
                                        height=4)
    lives_counter = LivesCounter(
        x=deliveries_counter_background.x + (deliveries_counter_background.length - 32),
        y=(deliveries_counter_background.y + deliveries_counter_background.height) + 5,
        length=32,
        height=16,
    )
    lives_counter_hanger = Element(x=lives_counter.x, y=lives_counter.y - 5, length=lives_counter.length, height=5)
    eliminates_deliveries_amount = Element(x=deliveries_counter_background.x + 3,
                                           y=deliveries_counter.y,
                                           length=6,
                                           height=11)
    rendered_eliminates_deliveries_amount = PyxelElement(eliminates_deliveries_amount,
                                                         Frame(0, 53, 18, 6, 11, 11))

    boss = Boss(57, running_window.height - 29, 12, 14)
    door = Door(57, running_window.height - 35, 10, 15, boss=boss)

    for i in range(selected_difficulty.difficulty_values()["belts"]):
        if i != (selected_difficulty.difficulty_values()["belts"] - 1):
            conveyors[i].next_step = conveyors[i + 1]
        else:
            conveyors[i].next_step = truck
    factory_conveyor.next_step = conveyors[0]

    package_factory = PackageFactory(
        running_window.width - 113 + factory_conveyor.length - 20,
        running_window.height - 113,
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

    conveyor_middle_frames = [Frame(1, 16, 88, 16, 8, colkey=0) for i in range(35)]
    conveyor_middle_frames_factory = [Frame(1, 16, 88, 16, 8, colkey=0) for i in range(5)]
    rendered_conveyors = [
        PyxelElement(
            conveyors[i],
            Frame(1, 0, 24, 8, 8, colkey=0),
            *conveyor_middle_frames,
            Frame(1, 0, 32, 16, 8, colkey=0),
            grid=Grid.ROW,
        )
        for i in range(selected_difficulty.difficulty_values()["belts"])
    ]
    # Static elements
    conveyor_transformers_frames = [
        Frame(1, 32, 16 + i * 16, 16, 16, colkey=0, scale=2)
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
    luigi_static_ladders_frames = [
        PyxelStaticElement(
            48,
            (running_window.height - 102 - i * 48),
            Frame(1, 0, 88, 16, 16, colkey=0, scale=3),
        )
        for i in range(selected_difficulty.difficulty_values()["belts"] - 1)
    ]
    mario_static_ladder_frames = [
        PyxelStaticElement(
            running_window.width - 85 if i != 0 else running_window.width - 95,
            (running_window.height - 102 - i * 48) if i != 0 else (running_window.height - 110),
            Frame(1, 0, 88, 16, 16, colkey=0, scale=(3 if i != 0 else 2)),
        )
        for i in range(selected_difficulty.difficulty_values()["belts"] - 1)
    ]

    luigi_static_ladders_platforms = [
        PyxelStaticElement(
            76,
            (running_window.height - 69 - i * 50),
            Frame(1, 0, 104, 16, 3, scale=2),
        )
        for i in range(selected_difficulty.difficulty_values()["belts"] - 1)
    ]

    mario_static_ladders_platforms = [
        PyxelStaticElement(
            running_window.width - 84,
            (running_window.height - 125 - i * 50),
            Frame(1, 0, 104, 24, 8, scale=2),
        )
        for i in range(selected_difficulty.difficulty_values()["belts"] - 2)
    ]
    static_ladders_pomost = [
        PyxelStaticElement(
            80,
            (running_window.height - 74 - i * 50),
            Frame(1, 0, 104, 8, 3, scale=4),
        )
        for i in range(selected_difficulty.difficulty_values()["belts"])
    ]
    static_ladders_platforms_for_ladders = [
        PyxelStaticElement(
            50,
            (running_window.height - 69 - i * 50),
            Frame(1, 0, 104, 16, 3, scale=2),
        )
        for i in range(selected_difficulty.difficulty_values()["belts"])
    ]
    static_ladders_platforms_for_ladders.pop(-1)

    game_app = GameApp(
        # Static Elements
        *luigi_static_ladders_frames,
        *mario_static_ladder_frames,
        *luigi_static_ladders_platforms,
        *mario_static_ladders_platforms,
        *static_ladders_platforms_for_ladders,
        *static_ladders_pomost,
        # Stairs
        PyxelStaticElement(
            300, running_window.height - 16 * 4 + 21, Frame(1, 48, 8, 40, 24, colkey=0, scale=3)
        ),

        # Dynamic Elements
        (PyxelElement(mario, Frame(0, 19, 1, 11, 14, scale=2, colkey=0))),
        (PyxelElement(luigi, Frame(0, 2, 1, 10, 14, scale=2, colkey=0))),
        (PyxelElement(package_factory, Frame(0, 64, 96, 60, 40, colkey=11))),
        *rendered_conveyors,
        PyxelElement(
            factory_conveyor,
            Frame(1, 0, 24, 8, 8, colkey=0),
            *conveyor_middle_frames_factory,
            Frame(1, 0, 32, 16, 8, colkey=0),
            grid=Grid.ROW,
        ),
        PyxelElement(truck, Frame(0, 131, 1, 45, 30, colkey=11)),
        PyxelElement(point_counter_background, Frame(0, 96, 139, 47, 21, colkey=0)),
        PyxelElement(
            point_counter,
            Frame(0, 53, 18, 6, 11, 11),
            Frame(0, 53, 18, 6, 11, 11),
            Frame(0, 53, 18, 6, 11, 11),
            Frame(0, 53, 18, 6, 11, 11),
            grid=Grid.ROW,
        ),
        PyxelElement(lives_counter_hanger, Frame(0, 64, 139, 32, 5, colkey=0)),
        PyxelElement(lives_counter, Frame(0, 64, 144, 32, 16)),
        PyxelElement(deliveries_counter_hanger, Frame(0, 96, 139, 47, 4, colkey=0)),
        PyxelElement(deliveries_counter_background, Frame(0, 96, 176, 47, 17)),
        PyxelElement(deliveries_counter, Frame(0, 53, 18, 5, 11, 11)),
        rendered_eliminates_deliveries_amount,
        PyxelElement(door, Frame(1, 19, 1, 10, 15, colkey=0, scale=3)),
        *static_conveyor_frames,
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
        move_package_tick=0.09,
        create_package_tick=5,
        selected_difficulty=selected_difficulty,
        app=app
    )

    return game_app
