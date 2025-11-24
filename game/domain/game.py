from game.domain.conveyor import Conveyor
from game.domain.exceptions import DomainError
from game.domain.floor import Floor
from game.domain.package import Package
from game.domain.package_factory import PackageFactory
from game.domain.player import Player
from game.domain.truck import Truck


class Game:
    def __init__(
        self,
        players: dict[Player, list[Floor, ...]],
        conveyors: list[Conveyor] | None = None,
        factories: list[PackageFactory] | None = None,
        truck: Truck = None
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
        self.truck = truck

    def move_packages(self) -> None:
        for conveyor in self.conveyors:
            for package in conveyor.packages:
                if conveyor.package_about_to_fall(package):
                    if conveyor.finish_floor.player is not None:
                        current_player = conveyor.finish_floor.player
                        if conveyor.next_step is None:
                            raise DomainError("next step is not defined for the conveyor")
                        else:
                            if isinstance(conveyor.next_step, Truck):
                                conveyor.next_step.put_package(package)
                                self.points += 2
                                conveyor.packages.remove(package)
                                self.packages_at_play -= 1
                            else:
                                conveyor.next_step.put_package(package)
                                current_player.pick_package(package)
                                self.points += 1
                                # FIXME short break between picking and putting package. maybe 2 move ticks
                                current_player.put_package()
                                conveyor.packages.remove(package)

        for conveyor in self.conveyors:
            conveyor.move_packages()

        self.tick += 1

    def move_player_up(self, player: Player) -> None:
        player_positions = self.players_positions[player]
        current_position_index = None
        for possible_player_position in player_positions:
            if possible_player_position.x == player.x and possible_player_position.y == player.y:
                current_position_index = player_positions.index(possible_player_position)

        if current_position_index is None:
            raise DomainError("Could not find the players current floor")

        if current_position_index == (len(player_positions)-1):
            return None
        else:
            player.move(player_positions[current_position_index+1].x, player_positions[current_position_index+1].y)
            player_positions[current_position_index].player = None
            player_positions[current_position_index+1].player = player
            return None

    def create_package(self):
        for factory in self.factories:
            self.newly_created_packages.append(factory.create_package())

    def move_player_down(self, player: Player) -> None:
        player_positions = self.players_positions[player]
        current_position_index = None
        for possible_player_position in player_positions:
            if possible_player_position.x == player.x and possible_player_position.y == player.y:
                current_position_index = player_positions.index(possible_player_position)

        if current_position_index is None:
            raise DomainError("Could not find the players current floor")

        if current_position_index == 0:
            return None
        else:
            player.move(player_positions[current_position_index - 1].x, player_positions[current_position_index - 1].y)
            player_positions[current_position_index].player = None
            player_positions[current_position_index - 1].player = player
            return None

    def give_points(self, game, amount: int):
        if not isinstance(game, Game):
            raise DomainError("game is not a Game class")
        else:
            game.points += amount