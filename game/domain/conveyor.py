from game.domain.directions import Direction
from game.domain.elements import Element
from game.domain.floor import Floor
from game.domain.logging import get_logger
from game.domain.package import CanRecievePackage, Package, PackageState
from game.domain.difficulty import selected_difficulty


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
        if conveyor_id == 0:
            self.direction = Direction.LEFT
        else:
            self.direction = Direction.RIGHT if conveyor_id % 2 == 0 else Direction.LEFT
        if conveyor_id == 0:
            self.velocity = speed[0]
        elif conveyor_id % 2 == 0:
            self.velocity = speed[1]
        else:
            self.velocity = speed[2]
        self.finish_floor = finish_floor
        self.falling_packages: list[Package] = []
        self.next_step = next_step
        self.packages: list[Package] = []
        if conveyor_id == 0:
            start_position: tuple[int, int] = (x + length - 16, y)
        elif self.direction == Direction.LEFT:
            start_position = (x + length - 12, y)
        else:
            start_position = (x, y)
        self.start_position: tuple[int, int] = start_position
        super().__init__(x, y, length, height)

    def put_package(self, package: Package) -> None:
        if not isinstance(package, Package):
            raise TypeError("package must be a Package instance")
        package.move(self.start_position[0], self.start_position[1] - package.height)
        package.state = PackageState.ON_CONVEYOR
        self.packages.append(package)

    def move_packages(self) -> None:
        """Move all packages on the conveyor according to its direction and velocity."""
        for package in self.packages:
            if package.stage != 5 and self._package_changes_stage(package):
                if package.stage == 0:
                    package.stage = 1
                    package.stage_to_be_changed_to = 1
                    logger.debug("%s increased stage to 1 of", package)
                elif package.stage == 1:
                    package.stage = 2
                    package.stage_to_be_changed_to = 2
                    logger.debug("%s increased stage to 1 of", package)
                elif package.stage == 2:
                    package.stage = 3
                    package.stage_to_be_changed_to = 3
                    logger.debug("%s increased stage to 1 of", package)
                elif package.stage == 3:
                    package.stage = 4
                    package.stage_to_be_changed_to = 4
                    logger.debug("%s increased stage to 1 of", package)
                elif package.stage == 4:
                    package.stage = 5
                    package.stage_to_be_changed_to = 5
                    logger.debug("%s increased stage to 1 of", package)

            if not package.state == PackageState.FALLING:
                if self.direction == Direction.LEFT:
                    package.move_x(package.x + self.velocity * -4)
                else:
                    package.move_x(package.x + self.velocity * 4)

            if not self._is_package_on_conveyor(package):
                logger.debug("%s felt", package)
                self.falling_packages.append(package)
                package.state = PackageState.FALLING
                if package.x < self.x:
                    package.state_to_be_changed_to = 1
                elif package.x + package.length > self.x + self.length:
                    package.state_to_be_changed_to = 2
                self.lift_package(package)
        for package in self.falling_packages:
            if self._package_is_offscreen(package):
                self.falling_packages.remove(package)
                logger.debug("%s due to being offscreen removed package", package)
                package.offscreen = True
            else:
                package.move_y(package.y + 4)

    def lift_package(self, package: Package) -> None:
        self.packages.remove(package)

    def _is_package_on_conveyor(self, package: Package) -> bool:
        return self.x <= package.x + (package.length // 2) + 1 <= self.x + self.length

    def _package_changes_stage(self, package: Package) -> bool:
        if self.conveyor_id % 2 != 0:
            return self.conveyor_id - 1 == package.stage and package.x <= self.x + (
                self.length // 2
            )
        elif self.conveyor_id % 2 == 0:
            return (
                self.conveyor_id - 1 == package.stage
                and package.x + package.length >= self.x + (self.length // 2)
            )
        raise ValueError("conveyor id is not valid")

    def _package_is_offscreen(self, package: Package) -> bool:
        if (
            package.y >= selected_difficulty.difficulty_values()["window_height"]
            or (package.x + package.length <= 0)
            or (package.x >= selected_difficulty.difficulty_values()["window_width"])
        ):
            return True
        else:
            return False

    def package_about_to_fall(self, package: Package) -> bool:
        return package.x <= (self.x - 1) or (self.x + self.length + 1) <= (
            package.x + package.length
        )
