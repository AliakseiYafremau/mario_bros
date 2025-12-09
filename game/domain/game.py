from game.domain.conveyor import Conveyor
from game.domain.exceptions import DomainError
from game.domain.floor import Floor
from game.domain.package import Package
from game.domain.package_factory import PackageFactory
from game.domain.player import Player
from game.domain.truck import Truck
from game.presentation.gui import PointsCounter


class Game:
    """Core class that coordinates conveyors, players, factories, and the truck.

    This class contains the main game logic: it moves packages along conveyors,
    handles player actions, manages scoring, lives and deliveries, and interacts
    with the truck and the GUI.

    Attributes:
        players (tuple[Player, ...]): The players participating in the game.
        players_positions (dict[Player, list[Floor]]): The floors each player can stand on.
        conveyors (list[Conveyor]): The list of conveyors currently in the game.
        factories (list[PackageFactory]): The list of factories generating packages.
        truck (Truck): The truck where packages are finally delivered.
        point_counter (PointsCounter | None): GUI element to show points, if any.

        live_amount (int): Number of lives remaining. Must be >= 0.
        points (int): Current score. Must be >= 0.
        stored_deliveries (int): Number of deliveries not used for healing. Must be >= 0.
        minimum_number_packages (int): Minimum number of packages in play. Must be >= 0.
        packages_at_play (int): Number of packages currently in play. Must be >= 0.

        Other bool flags used only for indicating UI updates and special events.
    """

    def __init__(
        self,
        players: dict[Player, list[Floor]],
        truck: Truck,
        conveyors: list[Conveyor] | None = None,
        factories: list[PackageFactory] | None = None,
        point_counter: PointsCounter | None = None,
    ) -> None:
        """Initializes the game, checking coherence of players and floors.

        :param players: dict mapping each Player to the list of Floors they can stand on.
        :param truck: Truck, the truck where packages are delivered.
        :param conveyors: optional list of Conveyor instances.
        :param factories: optional list of PackageFactory instances.
        :param point_counter: optional GUI points counter.
        :raises DomainError: if a player is not located on one of the entered floors.
        """
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

    # live_amount
    @property
    def live_amount(self) -> int:
        """Returns the number of lives remaining.

        :return: int, the number of lives (>= 0).
        """
        return self.__live_amount

    @live_amount.setter
    def live_amount(self, value: int) -> None:
        """Sets the number of lives remaining.

        :param value: int, new number of lives. Must be >= 0.
        :raises TypeError: if value is not an int.
        :raises ValueError: if value is negative.
        """
        if not isinstance(value, int):
            raise TypeError("live_amount must be an int")
        if value < 0:
            raise ValueError("live_amount cannot be negative")
        self.__live_amount = value

    # points
    @property
    def points(self) -> int:
        """Returns the current score.

        :return: int, the current points (>= 0).
        """
        return self.__points

    @points.setter
    def points(self, value: int) -> None:
        """Sets the current score.

        :param value: int, new score. Must be >= 0.
        :raises TypeError: if value is not an int.
        :raises ValueError: if value is negative.
        """
        if not isinstance(value, int):
            raise TypeError("points must be an int")
        if value < 0:
            raise ValueError("points cannot be negative")
        self.__points = value

    # stored_deliveries
    @property
    def stored_deliveries(self) -> int:
        """Returns the number of stored deliveries.

        :return: int, number of successful deliveries (>= 0).
        """
        return self.__stored_deliveries

    @stored_deliveries.setter
    def stored_deliveries(self, value: int) -> None:
        """Sets the number of stored deliveries.

        :param value: int, new number of deliveries. Must be >= 0.
        :raises TypeError: if value is not an int.
        :raises ValueError: if value is negative.
        """
        if not isinstance(value, int):
            raise TypeError("stored_deliveries must be an int")
        if value < 0:
            raise ValueError("stored_deliveries cannot be negative")
        self.__stored_deliveries = value

    # minimum_number_packages
    @property
    def minimum_number_packages(self) -> int:
        """Returns the minimum number of packages that should be in play.

        :return: int, minimum number of packages (>= 0).
        """
        return self.__minimum_number_packages

    @minimum_number_packages.setter
    def minimum_number_packages(self, value: int) -> None:
        """Sets the minimum number of packages that should be in play.

        :param value: int, new minimum number of packages. Must be >= 0.
        :raises TypeError: if value is not an int.
        :raises ValueError: if value is negative.
        """
        if not isinstance(value, int):
            raise TypeError("minimum_number_packages must be an int")
        if value < 0:
            raise ValueError("minimum_number_packages cannot be negative")
        self.__minimum_number_packages = value

    # packages_at_play
    @property
    def packages_at_play(self) -> int:
        """Returns the number of packages currently in play.

        :return: int, number of packages in play (>= 0).
        """
        return self.__packages_at_play

    @packages_at_play.setter
    def packages_at_play(self, value: int) -> None:
        """Sets the number of packages currently in play.

        :param value: int, new number of packages in play. Must be >= 0.
        :raises TypeError: if value is not an int.
        :raises ValueError: if value is negative.
        """
        if not isinstance(value, int):
            raise TypeError("packages_at_play must be an int")
        if value < 0:
            raise ValueError("packages_at_play cannot be negative")
        self.__packages_at_play = value

    def move_packages(self) -> None:
        """Moves packages across conveyors and handles pickups by players.

        This method:
          * checks if packages are about to fall and lets players pick them up,
          * moves all packages on each conveyor,
          * updates flags to indicate changes in conveyor or truck.
        :raises DomainError: if a conveyor has no defined next_step.
        """
        for conveyor in self.conveyors:
            for package in list(conveyor.packages):
                if conveyor.package_about_to_fall(package):
                    if conveyor.finish_floor.player is not None:
                        if conveyor.next_step is None:
                            raise DomainError(
                                "next step is not defined for the conveyor"
                            )
                        if conveyor.finish_floor.player.pick_package(package):
                            conveyor.finish_floor.player.sprite_to_be_changed = True
                            conveyor.packages.remove(package)
                            if conveyor.next_step != self.truck:
                                self.package_changes_conveyor = True

        for conveyor in self.conveyors:
            conveyor.move_packages()

    def player_put_down_package(self, player: Player) -> None:
        """Places the package carried by a player on the corresponding conveyor/truck.

        If the player stands on a floor that is the end of a conveyor, the package is
        put on the conveyor's next step. Points and packages_at_play are updated.

        :param player: Player, the player that is putting down a package.
        :raises DomainError: if the player does not carry a package or the conveyor has no next_step.
        """
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
        """Moves a player one floor up if possible.

        :param player: Player, the player to move upwards.
        :raises DomainError: if the player's current floor cannot be found.
        """
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
            return
        player.move(
            player_positions[current_position_index + 1].x,
            player_positions[current_position_index + 1].y,
        )
        player_positions[current_position_index].player = None
        player_positions[current_position_index + 1].player = player

    def create_package(self) -> None:
        """Creates new packages using all factories.

        Newly created packages are appended to the `newly_created_packages` list.
        """
        for factory in self.factories:
            self.newly_created_packages.append(factory.create_package())

    def move_player_down(self, player: Player) -> None:
        """Moves a player one floor down if possible.

        :param player: Player, the player to move downwards.
        :raises DomainError: if the player's current floor cannot be found.
        """
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
            return
        player.move(
            player_positions[current_position_index - 1].x,
            player_positions[current_position_index - 1].y,
        )
        player_positions[current_position_index].player = None
        player_positions[current_position_index - 1].player = player
