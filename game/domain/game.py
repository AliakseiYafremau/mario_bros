from game.domain.conveyor import Conveyor
from game.domain.exceptions import DomainError
from game.domain.floor import Floor
from game.domain.package import Package
from game.domain.package_factory import PackageFactory
from game.domain.player import Player


class Game:
    def __init__(
        self,
        players: dict[Player, list[Floor, ...]],
        conveyors: list[Conveyor] | None = None,
        factories: list[PackageFactory] | None = None,
    ) -> None:
        self.tick = 0
        self.newly_created_packages: list[Package] = []
        self.live_amount = 3
        self.points = 0
        self.stored_deliveries = 0
        self.minimum_number_packages = 1

        for player in players.keys():
            is_correct = False
            if Floor(player.x, player.y) in players[player]:
                is_correct = True
            if not is_correct:
                raise DomainError("player is not located on one of the entered points")

        self.players = tuple(players.keys())
        self.players_positions = players
        self.conveyors = conveyors if conveyors is not None else []
        self.factories = factories if factories is not None else []
        self.packages_at_play = 0
        self.packages = []

    def move_packages(self) -> None:
        for conveyor in self.conveyors:
            if conveyor.falling_package is not None:
                if conveyor.finish_floor.player is not None:
                    current_package = conveyor.falling_package
                    current_player = conveyor.finish_floor.player
                    next_step = conveyor.next_step
                    if next_step is None:
                        raise DomainError("next step is not defined for the conveyor")

                    # FIXME Does not make sense to pick and put at the same time
                    # P.S we can use it for the representation that depends of the state
                    current_player.pick_package(current_package)
                    current_player.put_package()

                    next_step.put_package(current_package)
                else:
                    self.live_amount -= 1
                    if self.live_amount < 0:
                        raise DomainError("no more lives left")
                conveyor.falling_package = None

        for conveyor in self.conveyors:
            conveyor.move_packages()

        self.tick += 1

    def move_player_up(self, player: Player) -> None:
        player_positions = self.players_positions[player]
        player_current_floor = Floor(player.x, player.y)

        if player_current_floor == player_positions[-1]:
            raise DomainError("cannot raise the player because is on the top")

        for position_index in range(len(player_positions) - 1):
            if player_current_floor == player_positions[position_index]:
                new_player_position = player_positions[position_index + 1]
                player.move(new_player_position.x, new_player_position.y)
                return

        raise DomainError("player has invalid position")

    def create_package(self):
        for factory in self.factories:
            self.newly_created_packages.append(factory.create_package())

    def move_player_down(self, player: Player) -> None:
        player_positions = self.players_positions[player]
        player_current_floor = Floor(player.x, player.y)

        if player_current_floor == player_positions[0]:
            raise DomainError("cannot lower the player because is on the bottom")

        for position_index in range(1, len(player_positions)):
            if player_current_floor == player_positions[position_index]:
                new_player_position = player_positions[position_index - 1]
                player.move(new_player_position.x, new_player_position.y)
                return

        raise DomainError("player has invalid position")
