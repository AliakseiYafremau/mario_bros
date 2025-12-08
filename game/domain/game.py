from game.domain.conveyor import Conveyor
from game.domain.exceptions import DomainError
from game.domain.floor import Floor
from game.domain.package import Package
from game.domain.package_factory import PackageFactory
from game.domain.player import Player
from game.domain.truck import Truck
from game.presentation.gui import PointsCounter



class Game:
    """Core domain service that coordinates conveyors, players, factories, and the truck."""

    def __init__(
        self,
        players: dict[Player, list[Floor]],
        truck: Truck,
        conveyors: list[Conveyor] | None = None,
        factories: list[PackageFactory] | None = None,
        point_counter: PointsCounter | None = None,
    ) -> None:
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
        self.original_truck_x = truck.x
        self.first_package_moved = False
        self.point_counter = point_counter
        self.points_to_be_updated = False
        self.lives_to_be_updated = False
        self.deliveries_to_be_updated = False
        self.boss_comes_in = False
        self.package_changes_conveyor = False
        self.package_put_in_truck = False

    def move_packages(self) -> None:
        for conveyor in self.conveyors:
            for package in conveyor.packages:
                if conveyor.package_about_to_fall(package):
                    if conveyor.finish_floor.player is not None:
                        if conveyor.next_step is None:
                            raise DomainError(
                                "next step is not defined for the conveyor"
                            )
                        elif conveyor.finish_floor.player.pick_package(package):
                            conveyor.finish_floor.player.sprite_to_be_changed = True
                            conveyor.packages.remove(package)
                            if conveyor.next_step != self.truck:
                                self.package_changes_conveyor = True

        for conveyor in self.conveyors:
            conveyor.move_packages()

    def player_put_down_package(self, player: Player) -> None:
        for conveyor in self.conveyors:
            if conveyor.finish_floor.player == player:
                package = player.package
                if package is None:
                    raise DomainError("player does not carry a package")
                if conveyor.next_step is None:
                    raise DomainError("next step is not defined for the conveyor")
                conveyor.next_step.put_package(package)
                player.put_package()
                if isinstance(conveyor.next_step, Truck):
                    self.packages_at_play -= 1
                    self.points += 2
                    self.package_put_in_truck = True
                else:
                    self.first_package_moved = True
                    self.points += 1
                self.points_to_be_updated = True

    def move_player_up(self, player: Player) -> None:
        player_positions = self.players_positions[player]
        current_position_index = None
        for possible_player_position in player_positions:
            if (
                possible_player_position.x == player.x
                and possible_player_position.y == player.y
            ):
                current_position_index = player_positions.index(
                    possible_player_position
                )

        if current_position_index is None:
            raise DomainError("Could not find the players current floor")

        if current_position_index == (len(player_positions) - 1):
            return None
        else:
            player.move(
                player_positions[current_position_index + 1].x,
                player_positions[current_position_index + 1].y,
            )
            player_positions[current_position_index].player = None
            player_positions[current_position_index + 1].player = player
            return None

    def create_package(self):
        for factory in self.factories:
            self.newly_created_packages.append(factory.create_package())

    def move_player_down(self, player: Player) -> None:
        player_positions = self.players_positions[player]
        current_position_index = None
        for possible_player_position in player_positions:
            if (
                possible_player_position.x == player.x
                and possible_player_position.y == player.y
            ):
                current_position_index = player_positions.index(
                    possible_player_position
                )

        if current_position_index is None:
            raise DomainError("Could not find the players current floor")

        if current_position_index == 0:
            return None
        else:
            player.move(
                player_positions[current_position_index - 1].x,
                player_positions[current_position_index - 1].y,
            )
            player_positions[current_position_index].player = None
            player_positions[current_position_index - 1].player = player
            return None
