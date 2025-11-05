from game.domain.elements import MotionElement
from game.domain.exceptions import DomainError
from game.domain.package import Package, PackageState


class Player(MotionElement):
    def __init__(self, x, y, length, height, name):
        self.name = name
        self._package: Package | None = None
        super().__init__(x, y, length, height)

    @property
    def package(self):
        return self._package

    @package.setter
    def package(self, value):
        if not isinstance(value, Package) or (value is not None):
            raise TypeError("package must be a Package instance or None")
        self._package = value

    def pick_package(self, package: Package):
        if self.package is not None:
            raise DomainError("player already has a package")
        package.state = PackageState.PICKED
        self.package = package

    def put_package(self):
        if self.package is None:
            raise DomainError("player does not have any package")
        self.package.state = PackageState.FREE
        self.package = None

    def move(self, dx=0, dy=0):
        self.package.move(dx=dx, dy=dy)
        return super().move(dx, dy)

    def move_x(self, dx):
        return self.move(dx=dx, dy=0)

    def move_y(self, dy):
        return self.move(dx=0, dy=dy)
