from game.domain.elements import MotionElement
from game.domain.exceptions import DomainError
from game.domain.package import Package, PackageState


class Player(MotionElement):
    def __init__(self, x, y, length, height, name):
        self.name = name
        self.package: Package | None = None
        super().__init__(x, y, length, height)

    def take_package(self, package: Package):
        if not isinstance(package, Package):
            raise TypeError("package must be a Package instance")
        package.state = PackageState.PICKED
        self.package = package

    def put_package(self):
        if self.package is None:
            raise DomainError("player does not have any package")
        self.package.state = PackageState.FREE
        self.package = None
