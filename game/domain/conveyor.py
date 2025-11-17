from game.domain.directions import Direction
from game.domain.elements import Element
from game.domain.floor import Floor
from game.domain.logging import get_logger
from game.domain.package import Package, PackageState


logger = get_logger(__name__, layer="DOMAIN")


class Conveyor(Element):
    """The conveyor belt element.

    The `Conveyor` is an element that can move `Package` objects
    placed on it in a specified direction and velocity.

    Attributes:
        x (int): Current X coordinate.
        y (int): Current Y coordinate.
        length (int): Length of the conveyor in the X axis.
        height (int): Height of the conveyor in the Y axis.
        direction (Direction): Direction in which the conveyor moves packages.
        velocity (int): Speed at which the conveyor moves packages.
        start_floor (Floor): The floor where the conveyor starts.
        finish_floor (Floor): The floor where the conveyor ends.

    Raises:
        TypeError: If ``direction`` is not a :class:`Direction` instance.
        ValueError: If ``velocity`` is negative.
    """

    def __init__(
        self,
        x: int,
        y: int,
        length: int,
        height: int,
        direction: Direction,
        velocity: int,
        finish_floor: Floor,
        next_conveyor: "Conveyor | None" = None,
    ) -> None:
        self.direction = direction
        self.velocity = velocity
        self.finish_floor = finish_floor
        self.falling_package: Package | None = None
        self.next_conveyor = next_conveyor
        self._packages: list[Package] = []
        super().__init__(x, y, length, height)

    @property
    def velocity(self) -> int:
        return self._velocity

    @velocity.setter
    def velocity(self, value: int) -> None:
        if value < 0:
            raise ValueError("Velocity cannot be negative")
        self._velocity = value

    @property
    def direction(self) -> Direction:
        return self._direction

    @direction.setter
    def direction(self, value: Direction) -> None:
        if not isinstance(value, Direction):
            raise TypeError("direction must be a Direction instance")
        self._direction = value

    def move_packages(self) -> None:
        """Move all packages on the conveyor according to its direction and velocity."""
        for package in self._packages:
            if self.direction == Direction.LEFT:
                package.move_x(package.x + self._velocity * -1)
            else:
                package.move_x(package.x + self._velocity)
            if not self._is_package_on_conveyor(package):
                self.falling_package = package
                package.state = PackageState.FALLING
                self.lift_package(package)

    def put_package(self, package: Package) -> None:
        if not isinstance(package, Package):
            raise TypeError("package must be a Package instance")
        package.state = PackageState.ON_CONVEYOR
        self._packages.append(package)

    def lift_package(self, package: Package) -> None:
        self._packages.remove(package)

    def _is_package_on_conveyor(self, package: Package) -> bool:
        if self.x + self.length < package.x < self.x:
            return False
        return True
