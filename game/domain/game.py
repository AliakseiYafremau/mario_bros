from game.domain.conveyor import Conveyor
from game.domain.exceptions import DomainError
from game.domain.package import Package, PackageState
from game.domain.package_factory import PackageFactory
from game.domain.player import Player
from game.domain.truck import Truck


class Game:
    def __init__(
        self,
        live_amount: int,
        players: dict[Player, tuple[tuple[int, int], ...]],
        conveyors: list[Conveyor],
        packages: list[Package],
        factories: list[PackageFactory],
        trucks: list[Truck],
        gravity_force: int = -1,
    ):
        self.live_amount = live_amount

        for player in players.keys():
            is_correct = False
            if (player.x, player.y) in players[player]:
                is_correct = True
            if not is_correct:
                raise DomainError("player is not located on one of the entered points")

        self.players = players.keys()
        self.players_positions = players
        self.conveyors = conveyors
        self.packages = packages
        self.factories = factories
        self.trucks = trucks

        self.gravity_force = gravity_force

    def move_packages(self):
        falling_packages = self._give_falling_packages()
        free_packages = self._give_free_packages()

        for package in free_packages:
            for player in self.players:
                if player.is_touched(package) and player:
                    player.pick_package(package)
                    free_packages.remove(package)

        map(lambda package: package.move_x(self.gravity_force), falling_packages)
        map(lambda conveyor: conveyor.move_packages(), self.conveyors)

        fallen_packages = self._give_fallen_packages()
        self.live_amount -= len(fallen_packages)
        map(lambda package: self.packages.remove(package), fallen_packages)

    def move_player_up(self, player: Player):
        player_positions = self.players_positions[player]
        player_current_position = (player.x, player.y)

        if player_current_position == player_positions[-1]:
            raise DomainError("cannot raise the player because is on the top")

        for position_index in range(len(player_positions) - 1):
            if player_current_position == player_positions[position_index]:
                new_player_position = player_positions[position_index + 1]
                player.x, player.y = new_player_position[0], new_player_position[1]

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

        raise DomainError("player has invalid position")

    def _give_free_packages(self) -> list[Package]:
        return list(
            filter(lambda package: package.state == PackageState.FREE, self.packages)
        )

    def _give_falling_packages(self) -> list[Package]:
        return list(
            filter(lambda package: package.state == PackageState.FALLING, self.packages)
        )

    def _give_fallen_packages(self) -> list[Package]:
        return list(filter(lambda package: package.x < 0, self.packages))
