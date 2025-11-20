from game.domain.directions import Direction
from game.domain.elements import Element
from game.domain.floor import Floor
from game.domain.logging import get_logger
from game.domain.package import CanRecievePackage, Package, PackageState


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
        conveyor_id: int,
        x: int,
        y: int,
        length: int,
        height: int,
        speed: tuple,
        finish_floor: Floor,
        next_step: CanRecievePackage | None = None,
    ) -> None:
        self.conveyor_id = conveyor_id
        self.direction = Direction.LEFT if conveyor_id % 2 == 0 else Direction.RIGHT
        if conveyor_id == 0:
            self.velocity = speed[0]
        elif conveyor_id % 2 == 0:
            self.velocity = speed[1]
        else:
            self.velocity = speed[2]
        self.finish_floor = finish_floor
        self.falling_package: Package | None = None
        self.next_step = next_step
        self._packages: list[Package] = []
        if self.direction == Direction.LEFT:
            self.start_position: tuple[int, int] = (x+length, y)
        else:
            self.start_position = (x, y + height)
        super().__init__(x, y, length, height)

    def put_package(self, package: Package) -> None:
        if not isinstance(package, Package):
            raise TypeError("package must be a Package instance")
        package.move(self.start_position[0], self.start_position[1] - package.height)
        package.state = PackageState.ON_CONVEYOR
        self._packages.append(package)

    def move_packages(self) -> None:
        """Move all packages on the conveyor according to its direction and velocity."""
        for package in self._packages:
            if self.direction == Direction.LEFT:
                package.move_x(package.x + self.velocity * -5)
            else:
                package.move_x(package.x + self.velocity * 5)
            if not self._is_package_on_conveyor(package):
                logger.debug("%s felt", package)
                self.falling_package = package
                package.state = PackageState.FALLING
                self.lift_package(package)

    def lift_package(self, package: Package) -> None:
        self._packages.remove(package)

    def _is_package_on_conveyor(self, package: Package) -> bool:
        return self.x <= package.x <= self.x + self.length
