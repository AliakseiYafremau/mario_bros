from game.domain.conveyor import Conveyor
from game.domain.exceptions import DomainError
from game.domain.floor import Floor
from game.domain.package_factory import PackageFactory
from game.domain.player import Player
from game.domain.truck import Truck


class Game:
    def __init__(
        self,
        live_amount: int,
        players: dict[Player, tuple[Floor, ...]],
        conveyors: list[Conveyor] | None = None,
        factories: list[PackageFactory] | None = None,
    ) -> None:
        self.live_amount = live_amount
        self.tick = 0

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

    def move_packages(self) -> None:
        if self.tick >= 5:
            self.create_package()
            self.tick = 0

        for conveyor in self.conveyors:
            if conveyor.falling_package is not None:
                if conveyor.finish_floor.player is not None:
                    current_package = conveyor.falling_package
                    current_player = conveyor.finish_floor.player
                    if conveyor.next_conveyor is None:
                        raise DomainError("conveyor has no next conveyor")
                    next_conveyor = conveyor.next_conveyor

                    # FIXME Does not make sense to pick and put at the same time
                    # P.S we can use it for the representation that depends of the state
                    current_player.pick_package(current_package)
                    current_player.put_package()

                    next_conveyor.put_package(current_package)
                else:
                    self.live_amount -= 1
                conveyor.falling_package = None

        map(lambda conveyor: conveyor.move_packages(), self.conveyors)

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
            factory.create_package()

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
