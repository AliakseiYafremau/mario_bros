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
    
        gravity_force: int = -1,
    ):
        self.live_amount = live_amount
        self.players = players
        self.conveyors = conveyors
        self.packages = packages
        self.factories = factories
        self.trucks = trucks

        self.gravity_force =gravity_force

    def move_packages(self):
        fallen_packages = self.give_falling_packages()
        free_packages = self.give_free_packages()

        for package in free_packages:
            for player in self.players:
                if player.is_touched(package) and player:
                    player.pick_package(package)

        map(lambda package: package.move_x(self.gravity_force), fallen_packages)
        map(lambda conveyor: conveyor.move_packages(), self.conveyors)

    def give_free_packages(self) -> list[Package]:
        return list(
            filter(lambda package: package.staate == PackageState.FREE, self.packages)
        )

    def give_falling_packages(self) -> list[Package]:
        return list(
            filter(lambda package: package.state == PackageState.FALLING, self.packages)
        )