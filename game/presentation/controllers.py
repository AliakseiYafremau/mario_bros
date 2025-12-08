from abc import ABC, abstractmethod

from game.domain.exceptions import DomainError
from game.domain.game import Game
from game.domain.player import Player


class Controller(ABC):
    """Base command that binds keyboard events to in-game actions."""

    @abstractmethod
    def execute(self):
        """Execute the controller action."""
        pass


class MoveUpPlayer(Controller):
    """Controller that moves a bound player up one floor."""

    def __init__(self, game: Game, player: Player):
        self.game = game
        self.player = player

    def execute(self):
        try:
            self.game.move_player_up(self.player)
        except DomainError:
            return


class MoveDownPlayer(Controller):
    """Controller that moves a bound player down one floor."""

    def __init__(self, game: Game, player: Player):
        self.game = game
        self.player = player

    def execute(self):
        try:
            self.game.move_player_down(self.player)
        except DomainError:
            return
