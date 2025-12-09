from abc import ABC, abstractmethod

from game.domain.exceptions import DomainError
from game.domain.game import Game
from game.domain.player import Player


class Controller(ABC):
    """Base command that binds keyboard events to in-game actions.

    Subclasses must implement :meth:`execute` with the concrete
    behavior triggered by an input event.
    """

    @abstractmethod
    def execute(self) -> None:
        """Execute the controller action."""
        raise NotImplementedError


class MoveUpPlayer(Controller):
    """Controller that moves a bound player up one floor.

    Attributes:
        game (Game): The game instance that will perform the movement.
        player (Player): The player to move.
    """

    def __init__(self, game: Game, player: Player) -> None:
        """Initializes the controller with a game and a player.

        :param game: Game, the game instance.
        :param player: Player, the player to be moved upwards.
        :raises TypeError: if parameters have incorrect type.
        """
        self.game = game
        self.player = player

    @property
    def game(self) -> Game:
        """Returns the game associated with this controller.

        :return: Game, the game instance.
        """
        return self.__game

    @game.setter
    def game(self, game: Game) -> None:
        """Sets the game associated with this controller.

        :param game: Game, the game instance.
        :raises TypeError: if game is not a Game instance.
        """
        if not isinstance(game, Game):
            raise TypeError("game must be a Game instance")
        self.__game = game

    @property
    def player(self) -> Player:
        """Returns the player associated with this controller.

        :return: Player, the player instance.
        """
        return self.__player

    @player.setter
    def player(self, player: Player) -> None:
        """Sets the player associated with this controller.

        :param player: Player, the player instance.
        :raises TypeError: if player is not a Player instance.
        """
        if not isinstance(player, Player):
            raise TypeError("player must be a Player instance")
        self.__player = player

    def execute(self) -> None:
        """Moves the player up one floor, ignoring domain errors."""
        try:
            self.game.move_player_up(self.player)
        except DomainError:
            return


class MoveDownPlayer(Controller):
    """Controller that moves a bound player down one floor.

    Attributes:
        game (Game): The game instance that will perform the movement.
        player (Player): The player to move.
    """

    def __init__(self, game: Game, player: Player) -> None:
        """Initializes the controller with a game and a player.

        :param game: Game, the game instance.
        :param player: Player, the player to be moved downwards.
        :raises TypeError: if parameters have incorrect type.
        """
        self.game = game
        self.player = player

    @property
    def game(self) -> Game:
        """Returns the game associated with this controller.

        :return: Game, the game instance.
        """
        return self.__game

    @game.setter
    def game(self, game: Game) -> None:
        """Sets the game associated with this controller.

        :param game: Game, the game instance.
        :raises TypeError: if game is not a Game instance.
        """
        if not isinstance(game, Game):
            raise TypeError("game must be a Game instance")
        self.__game = game

    @property
    def player(self) -> Player:
        """Returns the player associated with this controller.

        :return: Player, the player instance.
        """
        return self.__player

    @player.setter
    def player(self, player: Player) -> None:
        """Sets the player associated with this controller.

        :param player: Player, the player instance.
        :raises TypeError: if player is not a Player instance.
        """
        if not isinstance(player, Player):
            raise TypeError("player must be a Player instance")
        self.__player = player

    def execute(self) -> None:
        """Moves the player down one floor, ignoring domain errors."""
        try:
            self.game.move_player_down(self.player)
        except DomainError:
            return
