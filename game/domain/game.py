from game.domain.conveyor import Conveyor
from game.domain.exceptions import DomainError
from game.domain.floor import Floor
from game.domain.package import Package, PackageState
from game.domain.package_factory import PackageFactory
from game.domain.player import Player
from game.domain.truck import Truck


class Game:
    def __init__(
        self,
        live_amount: int,
        players: dict[Player, tuple[Floor, ...]],
        conveyors: list[Conveyor] | None = None,
        packages: list[Package] | None = None,
        factories: list[PackageFactory] | None = None,
        trucks: list[Truck] | None = None,
    ):
        self.live_amount = live_amount

        for player in players.keys():
            is_correct = False
            if (player.x, player.y) in players[player]:
                is_correct = True
            if not is_correct:
                raise DomainError("player is not located on one of the entered points")

        self.players = tuple(players.keys())
        self.players_positions = players
        self.conveyors = conveyors if conveyors is not None else []
        self.packages = packages if packages is not None else []
        self.factories = factories if factories is not None else []
        self.trucks = trucks if trucks is not None else []

    def move_packages(self):
        for conveyor in self.conveyors:
            if conveyor.falling_package is not None:
                if conveyor.finish_floor.player is not None:
                    conveyor.finish_floor.player.pick_package(
                        conveyor.falling_package
                    )
                else:
                    self.live_amount -= 1
                conveyor.falling_package = None


        map(lambda conveyor: conveyor.move_packages(), self.conveyors)

    def move_player_up(self, player: Player):
        player_positions = self.players_positions[player]
        player_current_position = (player.x, player.y)

        if player_current_position == player_positions[-1]:
            raise DomainError("cannot raise the player because is on the top")

        for position_index in range(len(player_positions) - 1):
            if player_current_position == player_positions[position_index]:
                new_player_position = player_positions[position_index + 1]
                player.x, player.y = new_player_position[0], new_player_position[1]
                return

        raise DomainError("player has invalid position")

    def move_player_down(self, player: Player):
        player_positions = self.players_positions[player]
        player_current_position = (player.x, player.y)

        if player_current_position == player_positions[0]:
            raise DomainError("cannot lower the player because is on the bottom")

        for position_index in range(1, len(player_positions)):
            if player_current_position == player_positions[position_index]:
                new_player_position = player_positions[position_index - 1]
                player.x, player.y = new_player_position[0], new_player_position[1]
                return

        raise DomainError("player has invalid position")