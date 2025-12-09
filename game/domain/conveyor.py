from enum import Enum

from game.domain.elements import Element
from game.domain.floor import Floor
from game.domain.package import CanRecievePackage, Package, PackageState


class Direction(Enum):
    """Directional options for conveyor belts."""

    RIGHT = "RIGHT"
    LEFT = "LEFT"


class Conveyor(Element):
    """The conveyor belt element.

    It can move `Package` objects placed on
    it in a specified direction and velocity.

    Attributes:
        conveyor_id (int): Identifier of this conveyor. Must be >= 0.
        x (int): Current x coordinate (non-negative).
        y (int): Current y coordinate (non-negative).
        length (int): Length of the conveyor in the x axis (positive).
        height (int): Height of the conveyor in the y axis (positive).
        direction (Direction): Direction in which the conveyor moves packages.
        velocity (float): Speed at which the conveyor moves packages. Must be > 0.
        finish_floor (Floor): The floor where the conveyor ends.
        floor_y (int): The y coordinate where packages are considered to be invisible.
        next_step (CanRecievePackage | None): Next element that receives packages.
        start_position (tuple[int, int]): Initial position where packages are placed.
        packages (list[Package]): Packages currently on this conveyor.
        falling_packages (list[Package]): Packages that are currently falling.

    Raises:
        TypeError: If parameters have incorrect type.
        ValueError: If numeric parameters have invalid values.
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
        floor_y: int,
        next_step: CanRecievePackage | None = None,
    ) -> None:
        """Initializes a new conveyor belt.

        :param conveyor_id: int, identifier of the conveyor. Must be >= 0.
        :param x: int, x coordinate, must be >= 0.
        :param y: int, y coordinate, must be >= 0.
        :param length: int, length of the conveyor, must be > 0.
        :param height: int, height of the conveyor, must be > 0.
        :param speed: tuple, speed presets (index depends on conveyor_id).
        :param finish_floor: Floor, the floor where the conveyor ends.
        :param floor_y: int, y coordinate of the floor used for falling detection, must be >= 0.
        :param next_step: an object implementing `put_package` or None.
        :raises TypeError: if some parameter type is wrong.
        :raises ValueError: if some numeric parameter has an invalid value.
        """
        super().__init__(x, y, length, height)

        self.conveyor_id = conveyor_id

        # Direction is derived from the conveyor_id
        if conveyor_id == 0:
            self.direction = Direction.LEFT
        else:
            self.direction = Direction.RIGHT if conveyor_id % 2 == 0 else Direction.LEFT

        # Velocity is selected from the speed tuple
        if conveyor_id == 0:
            self.velocity = speed[0]
        elif conveyor_id % 2 == 0:
            self.velocity = speed[1]
        else:
            self.velocity = speed[2]

        self.finish_floor = finish_floor
        self.next_step = next_step
        self.floor_y = floor_y
        self.falling_packages: list[Package] = []
        self.packages: list[Package] = []

        if conveyor_id == 0 or self.direction == Direction.LEFT:
            start_position: tuple[int, int] = (x + length - 12, y)
        else:
            start_position = (x, y)

        # start_position is considered internal and not guarded by a property
        self.start_position: tuple[int, int] = start_position

    # conveyor_id
    @property
    def conveyor_id(self) -> int:
        """Returns the identifier of this conveyor.

        :return: int, the conveyor id (>= 0).
        """
        return self.__conveyor_id

    @conveyor_id.setter
    def conveyor_id(self, conveyor_id: int) -> None:
        """Sets the identifier of this conveyor.

        :param conveyor_id: int, new id, must be >= 0.
        :raises TypeError: if conveyor_id is not an int.
        :raises ValueError: if conveyor_id is negative.
        """
        if not isinstance(conveyor_id, int):
            raise TypeError("conveyor_id must be an int")
        if conveyor_id < 0:
            raise ValueError("conveyor_id must be greater than or equal to 0")
        self.__conveyor_id = conveyor_id

    # direction
    @property
    def direction(self) -> Direction:
        """Returns the direction of this conveyor.

        :return: Direction, either Direction.LEFT or Direction.RIGHT.
        """
        return self.__direction

    @direction.setter
    def direction(self, direction: Direction) -> None:
        """Sets the direction of this conveyor.

        :param direction: Direction, new direction of the conveyor.
        :raises TypeError: if direction is not a Direction instance.
        """
        if not isinstance(direction, Direction):
            raise TypeError("direction must be an instance of Direction")
        self.__direction = direction

    # velocity
    @property
    def velocity(self) -> float:
        """Returns the velocity of the conveyor.

        :return: float, the velocity (must be strictly positive).
        """
        return self.__velocity

    @velocity.setter
    def velocity(self, velocity: float) -> None:
        """Sets the velocity of the conveyor.

        :param velocity: float, the new velocity. Must be > 0.
        :raises TypeError: if velocity is not a number.
        :raises ValueError: if velocity is not strictly positive.
        """
        if not isinstance(velocity, (int, float)):
            raise TypeError("velocity must be a number (int or float)")
        velocity = float(velocity)
        if velocity <= 0:
            raise ValueError("velocity must be strictly greater than 0")
        self.__velocity = velocity

    # finish_floor
    @property
    def finish_floor(self) -> Floor:
        """Returns the floor where the conveyor ends.

        :return: Floor, the floor at the end of the conveyor.
        """
        return self.__finish_floor

    @finish_floor.setter
    def finish_floor(self, finish_floor: Floor) -> None:
        """Sets the floor where the conveyor ends.

        :param finish_floor: Floor, the floor at the end of the conveyor.
        :raises TypeError: if finish_floor is not a Floor instance.
        """
        from game.domain.floor import Floor as FloorClass  # avoid circular import issues

        if not isinstance(finish_floor, FloorClass):
            raise TypeError("finish_floor must be a Floor instance")
        self.__finish_floor = finish_floor

    # next_step
    @property
    def next_step(self) -> CanRecievePackage | None:
        """Returns the next element that receives packages.

        :return: an object implementing `put_package` or None.
        """
        return self.__next_step

    @next_step.setter
    def next_step(self, next_step: CanRecievePackage | None) -> None:
        """Sets the next element that receives packages.

        :param next_step: an object implementing put_package, or None.
        :raises TypeError: if next_step is not None and does not offer put_package.
        """
        if next_step is not None and not hasattr(next_step, "put_package"):
            raise TypeError("next_step must implement a put_package(package) method or be None")
        self.__next_step = next_step

    # floor_y
    @property
    def floor_y(self) -> int:
        """Returns the floor y level used for falling detection.

        :return: int, the y coordinate of the floor level.
        """
        return self.__floor_y

    @floor_y.setter
    def floor_y(self, floor_y: int) -> None:
        """Sets the floor y level used for falling detection.

        :param floor_y: int, the y coordinate. Must be >= 0.
        :raises TypeError: if floor_y is not an int.
        :raises ValueError: if floor_y is negative.
        """
        if not isinstance(floor_y, int):
            raise TypeError("floor_y must be an int")
        if floor_y < 0:
            raise ValueError("floor_y cannot be negative")
        self.__floor_y = floor_y

    def put_package(self, package: Package) -> None:
        """Places a package on the conveyor at the start position.

        The package will be moved to the `start_position` of the conveyor and
        its state will be set to :class:`PackageState.ON_CONVEYOR`.

        :param package: Package, the package to be placed on the conveyor.
        :raises TypeError: if package is not a Package instance.
        """
        if not isinstance(package, Package):
            raise TypeError("package must be a Package instance")
        package.move(self.start_position[0], self.start_position[1] - package.height)
        package.state = PackageState.ON_CONVEYOR
        self.packages.append(package)

    def move_packages(self) -> None:
        """Moves all packages on the conveyor according to its direction and velocity.

        This method updates the stage of each package, changes their position
        according to the conveyor direction and velocity, and handles the
        logic for falling packages.
        """
        for package in list(self.packages):
            if package.stage != 5 and self._package_changes_stage(package):
                if package.stage == 0:
                    package.stage = 1
                    package.stage_to_be_changed_to = 1
                elif package.stage == 1:
                    package.stage = 2
                    package.stage_to_be_changed_to = 2
                elif package.stage == 2:
                    package.stage = 3
                    package.stage_to_be_changed_to = 3
                elif package.stage == 3:
                    package.stage = 4
                    package.stage_to_be_changed_to = 4
                elif package.stage == 4:
                    package.stage = 5
                    package.stage_to_be_changed_to = 5

            if package.state != PackageState.FALLING:
                if self.direction == Direction.LEFT:
                    package.move_x(package.x + self.velocity * -4)
                else:
                    package.move_x(package.x + self.velocity * 4)

            if not self._is_package_on_conveyor(package):
                self.falling_packages.append(package)
                package.state = PackageState.FALLING
                if package.x < self.x:
                    package.state_to_be_changed_to = 1
                elif package.x + package.length > self.x + self.length:
                    package.state_to_be_changed_to = 2
                self.lift_package(package)

        for package in list(self.falling_packages):
            if package.y >= self.floor_y:
                self.falling_packages.remove(package)
                package.offscreen = True
            else:
                package.move_y(package.y + 4)

    def lift_package(self, package: Package) -> None:
        """Removes a package from the conveyor.

        This is used when a package starts falling or is picked by a player.

        :param package: Package, the package to be removed.
        :raises ValueError: if the package is not in the conveyor's list.
        """
        try:
            self.packages.remove(package)
        except ValueError as error:
            raise ValueError("Package is not on this conveyor") from error

    def _is_package_on_conveyor(self, package: Package) -> bool:
        """Checks whether a package is still on top of the conveyor.

        :param package: Package, the package to check.
        :return: bool, True if the package is on the conveyor, False otherwise.
        """
        return self.x <= package.x + (package.length // 2) + 1 <= self.x + self.length

    def _package_changes_stage(self, package: Package) -> bool:
        """Checks whether the package needs to change its stage.

        Stages depend on the conveyor id and the package position.

        :param package: Package, the package whose stage is checked.
        :return: bool, True if the stage must change, False otherwise.
        :raises ValueError: if the conveyor id is not valid.
        """
        if self.conveyor_id % 2 != 0:
            return self.conveyor_id - 1 == package.stage and package.x <= self.x + (
                self.length // 2
            )
        if self.conveyor_id % 2 == 0:
            return (
                self.conveyor_id - 1 == package.stage
                and package.x + package.length >= self.x + (self.length // 2)
            )
        raise ValueError("conveyor id is not valid")

    def package_about_to_fall(self, package: Package) -> bool:
        """Checks whether a package is about to fall from the conveyor.

        :param package: Package, the package to check.
        :return: bool, True if the package will leave the conveyor on next move.
        """
        if package.x <= self.x - 1 or (
            self.x + self.length + 1
        ) <= (package.x + package.length):
            return True
        if (
            self.direction == Direction.LEFT
            and package.x
            + (self.velocity * -4)
            + (package.length // 2)
            + 1
            < self.x
        ):
            return True
        if (
            self.direction == Direction.RIGHT
            and package.x
            + (self.velocity * 4)
            + (package.length // 2)
            + 1
            > self.x + self.length
        ):
            return True
        return False
