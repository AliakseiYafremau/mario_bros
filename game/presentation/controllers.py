from abc import abstractmethod, ABC

from game.domain.exceptions import DomainError
from game.domain.game import Game
from game.domain.logging import get_logger
from game.domain.player import Player


logger = get_logger(__name__, layer="PRESENTATION")


class Controller(ABC):
    """Controller interface for handling user inputs."""

    @abstractmethod
    def execute(self):
        raise NotImplementedError


class MoveUpPlayer(Controller):
    def __init__(self, game: Game, player: Player):
        self.game = game
        self.player = player

    def execute(self):
        try:
            logger.debug("MoveUpPlayer button was pressed")
            self.game.move_player_up(self.player)
        except DomainError:
            return


class MoveDownPlayer(Controller):
    def __init__(self, game: Game, player: Player):
        self.game = game
        self.player = player

    def execute(self):
        try:
            logger.debug("MoveDownPlayer button was pressed")
            self.game.move_player_down(self.player)
        except DomainError:
            return


class SwitchSceneController(Controller):

    def __init__(self, manager, scene_name: str):
        self.manager = manager
        self.scene_name = scene_name

    def execute(self):
            self.manager.switch_to(self.scene_name)