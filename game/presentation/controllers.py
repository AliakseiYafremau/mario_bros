from abc import ABC, abstractmethod

from game.domain.exceptions import DomainError
from game.domain.game import Game
from game.domain.player import Player


class Controller(ABC):

    @abstractmethod
    def execute(self):
        pass


class MoveUpPlayer(Controller):
    def __init__(self, game: Game, player: Player):
        self.game = game
        self.player = player

    def execute(self):
        try:
            self.game.move_player_up(self.player)
        except DomainError:
            return


class MoveDownPlayer(Controller):
    def __init__(self, game: Game, player: Player):
        self.game = game
        self.player = player

    def execute(self):
        try:
            self.game.move_player_down(self.player)
        except DomainError:
            return
