import pyxel

from game.domain.conveyor import Conveyor
from game.domain.difficulty import Difficulty
from game.presentation.gui import Window
from game.domain.floor import Floor
from game.domain.game import Game
from game.domain.package_factory import PackageFactory
from game.domain.player import Player
from game.domain.truck import Truck
from game.presentation.app import PyxelApp
from game.presentation.controllers import MoveDownPlayer, MoveUpPlayer
from game.presentation.pyxel_elements import (
    BoardedPyxelElement,
    Frame,
    Grid,
    PyxelElement,
)


def main():
    mario = Player(200, 450, 16, 16, "Mario")
    luigi = Player(25, 450, 16, 16, "Luigi")

    selected_difficulty = Difficulty(0)  # Hard set since we are not going to actually implement a difficulty selector
    running_window = Window()

    floors_mario = [Floor(x=200, y=(running_window.height-50-i*50), player=mario) for i in range(selected_difficulty.difficulty_values()["belts"])]
    floors_luigi = [Floor(x=25, y=(running_window.height-50-i*50), player=luigi) for i in range(selected_difficulty.difficulty_values()["belts"])]
    floors = []
    for i in range(selected_difficulty.difficulty_values()["belts"]):
        floors.append((floors_luigi[i], floors_mario[i]))

    speed = selected_difficulty.difficulty_values()["conveyor_speed"]
    conveyors = [Conveyor(conveyor_id=i,
                          x=50,
                          y=(running_window.height-50-i*50),
                          length=200, height=20, speed=speed,
                          finish_floor=floors[i][i%2]
                          ) for i in range(selected_difficulty.difficulty_values()["belts"])]

    truck = Truck(
        x=50,
        y=50,
        length=50,
        height=50,
    )

    package_factory = PackageFactory(50, 50, 16, 16, 70, 150, 16, 16, conveyors[0])

    game = Game(
        live_amount=3,
        players={
            mario: floors_mario,
            luigi: floors_luigi,
        },
        conveyors=conveyors,
        factories=[package_factory],
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

    PyxelApp(BoardedPyxelElement(PyxelElement(mario, Frame(0, 0, 0, 16, 16))),
        BoardedPyxelElement(PyxelElement(luigi, Frame(0, 16, 0, 16, 16))),
        BoardedPyxelElement(
            PyxelElement(
                conveyors[0],
                Frame(1, 0, 24, 8, 8),
                Frame(1, 16, 88, 16, 8),
                Frame(1, 16, 88, 16, 8),
                Frame(1, 16, 88, 16, 8),
                Frame(1, 16, 88, 16, 8),
                Frame(1, 16, 88, 16, 8),
                Frame(1, 16, 88, 16, 8),
                Frame(1, 16, 88, 16, 8),
                Frame(1, 16, 88, 16, 8),
                Frame(1, 16, 88, 16, 8),
                Frame(1, 16, 88, 16, 8),
                Frame(1, 0, 32, 16, 8),
                grid=Grid.ROW,
            )
        ),
        BoardedPyxelElement(
            PyxelElement(
                conveyors[1],
                Frame(1, 0, 24, 8, 8),
                Frame(1, 16, 88, 16, 8),
                Frame(1, 16, 88, 16, 8),
                Frame(1, 16, 88, 16, 8),
                Frame(1, 16, 88, 16, 8),
                Frame(1, 16, 88, 16, 8),
                Frame(1, 16, 88, 16, 8),
                Frame(1, 16, 88, 16, 8),
                Frame(1, 16, 88, 16, 8),
                Frame(1, 16, 88, 16, 8),
                Frame(1, 16, 88, 16, 8),
                Frame(1, 0, 32, 16, 8),
                grid=Grid.ROW,
            )
        ),
        BoardedPyxelElement(
            PyxelElement(
                conveyors[2],
                Frame(1, 0, 24, 8, 8),
                Frame(1, 16, 88, 16, 8),
                Frame(1, 16, 88, 16, 8),
                Frame(1, 16, 88, 16, 8),
                Frame(1, 16, 88, 16, 8),
                Frame(1, 16, 88, 16, 8),
                Frame(1, 16, 88, 16, 8),
                Frame(1, 16, 88, 16, 8),
                Frame(1, 16, 88, 16, 8),
                Frame(1, 16, 88, 16, 8),
                Frame(1, 16, 88, 16, 8),
                Frame(1, 0, 32, 16, 8),
                grid=Grid.ROW,
            )
        ),
        BoardedPyxelElement(
            PyxelElement(
                package_factory,
                Frame(0, 80, 0, 16, 16),
            )
        ),
        buttons={
            pyxel.KEY_UP: move_up_mario,
            pyxel.KEY_DOWN: move_down_mario,
            pyxel.KEY_W: move_up_luigi,
            pyxel.KEY_S: move_down_luigi,
        },
        game=game,
        tick_second=1,
        move_package_tick=1,
        create_package_tick=5,
    )


if __name__ == "__main__":
    main()
