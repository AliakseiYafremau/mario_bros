from game.domain.conveyor import Conveyor
from game.domain.package import Package, PackageState
from game.domain.package_factory import PackageFactory
from game.domain.player import Player
from game.domain.truck import Truck


class Game:
    def __init__(
        self,
        live_amount: int,
        players: list[Player],
        conveyors: list[Conveyor],
        packages: list[Package],
        factories: list[PackageFactory],
        trucks: list[Truck],
    ):
        self.live_amount = live_amount
        self.players = players
        self.conveyors = conveyors
        self.packages = packages
        self.factories = factories
        self.trucks = trucks

    def move(self):
        falling_packages = self.give_falling_packages()
        free_packages = self.give_free_packages()

        # ...

    def give_free_packages(self):
        return list(
            filter(lambda package: package.staate == PackageState.FREE, self.packages)
        )

    def give_falling_packages(self):
        return list(
            filter(lambda package: package.state == PackageState.FALLING, self.packages)
        )

    def can_player_take_package(self, package: Package):
        return True # Fake implementation