from game.domain.directions import Direction
from game.domain.elements import Element
from game.domain.package import Package, PackageState


class Conveyor(Element):
    def __init__(
        self,
        x: int,
        y: int,
        length: int,
        height: int,
        direction: Direction,
        velocity: int,
    ):
        self.direction = direction
        self.velocity = velocity
        self._packages: list[Package] = []
        super().__init__(x, y, length, height)

    @property
    def velocity(self) -> int:
        return self._velocity

    @velocity.setter
    def velocity(self, value: int):
        if value < 0:
            raise ValueError("Velocity cannot be negative")
        self._velocity = value

    @property
    def direction(self) -> Direction:
        return self._direction

    @direction.setter
    def direction(self, value: Direction):
        if not isinstance(value, Direction):
            raise TypeError("direction must be a Direction instance")
        self._direction = value

    def move_packages(self):
        for package in self._packages:
            package.move_x(self._velocity)
            if not self._is_package_on_conveyor(package):
                self.lift_package(package)

    def put_package(self, package: Package):
        if not isinstance(package, Package):
            raise TypeError("package must be a Package instance")
        package.state = PackageState.ON_CONVEYOR
        self._packages.append(package)

    def lift_package(self, package: Package):
        self._packages.remove(package)
        package.state = PackageState.FREE

    def _is_package_on_conveyor(self, package: Package) -> bool:
        if self.x + self.length < package.x:
            return False
        return True

