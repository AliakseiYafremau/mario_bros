import pyxel

from game.domain.conveyor import Conveyor
from game.domain.directions import Direction
from game.domain.floor import Floor
from game.domain.game import Game
from game.domain.package_factory import PackageFactory
from game.domain.player import Player
from game.presentation.app import PyxelApp
from game.presentation.controllers import MoveDownPlayer, MoveUpPlayer
from game.presentation.pyxel_elements import BoardedPyxelElement, Frame, Grid, PyxelElement


def main():
    mario = Player(200, 100, 16, 16, "Mario")
    luigi = Player(100, 100, 100, 100, "Luigi")

    floor1_mario = Floor(200, 150)
    floor2_mario = Floor(200, 100)
    floor3_mario = Floor(200, 50, player=mario)

    floor1_luigi = Floor(100, 150)
    floor2_luigi = Floor(100, 100)
    floor3_luigi = Floor(100, 50, player=luigi)

    conveyor1 = Conveyor(
        x=50,
        y=150,
        length=100,
        height=20,
        direction=Direction.RIGHT,
        velocity=5,
        finish_floor=floor1_mario,
    )
    conveyor2 = Conveyor(
        x=150,
        y=150,
        length=100,
        height=20,
        direction=Direction.LEFT,
        velocity=5,
        finish_floor=floor1_luigi,
    )
    conveyor1.next_conveyor = conveyor2

    package_factory = PackageFactory(50, 50, 50, 50, 70, 150, 50, 50, conveyor1)

    game = Game(
        live_amount=3,
        players={
            mario: (floor1_mario, floor2_mario, floor3_mario),
            luigi: (floor1_luigi, floor2_luigi, floor3_luigi),
        },
        conveyors=[conveyor1, conveyor2],
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

    PyxelApp(
        BoardedPyxelElement(PyxelElement(mario, Frame(0, 0, 0, 16, 16))),
        PyxelElement(luigi, Frame(0, 16, 0, 16, 16)),
        PyxelElement(
            conveyor1,
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
        ),
        PyxelElement(
            package_factory,
            Frame(0, 80, 0, 16, 16),
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
