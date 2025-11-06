import pyxel
from game.domain.game import Game
from game.domain.player import Player
from game.presentation.app import PyxelApp
from game.presentation.controllers import MoveDownPlayer, MoveUpPlayer
from game.presentation.pyxel_elements import PyxelElement


def main():
    mario = Player(200, 100, 100, 100, "Mario")
    luigi = Player(100, 100, 100, 100, "Luigi")

    game = Game(
        live_amount=3,
        players={
            mario: ((200, 100), (200, 0)),
            luigi: ((100, 100), (100, 0))
        }
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
        PyxelElement(mario, 0, 0, 0, 16, 16),
        PyxelElement(luigi, 0, 0, 16, 16, 16),
        buttons={
            pyxel.KEY_UP: move_up_mario,
            pyxel.KEY_DOWN: move_down_mario,
            pyxel.KEY_W: move_up_luigi,
            pyxel.KEY_S: move_down_luigi,
        }
    )


if __name__ == "__main__":
    main()
