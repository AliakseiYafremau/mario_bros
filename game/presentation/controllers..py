from abc import abstractmethod, ABC

from game.domain.game import Game
from game.domain.player import Player


class Controller(ABC):
    @abstractmethod
    def execute(self):
        raise NotImplementedError


class MoveUpPlayer(Controller):
    def __init__(self, game: Game, player: Player):
        self.game = game
        self.player = player
    
    def execute(self):
        self.game.move_player_up(self.player)


class MoveDownPlayer(Controller):
    def __init__(self, game: Game, player: Player):
        self.game = game
        self.player = player
    
    def execute(self):
        self.game.move_player_down(self.player)