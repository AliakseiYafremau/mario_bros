from game.domain.elements import MotionElement
from game.domain.package import Package, PackageState


class Truck(MotionElement):
    """Movable delivery truck that accepts completed packages.

    The truck can move horizontally, load packages and determine if it is full.

    Attributes:
        x (int): Current x coordinate (non-negative).
        y (int): Current y coordinate (non-negative).
        length (int): Width of the truck (positive).
        height (int): Height of the truck (positive).
        packages (list[Package]): Packages loaded on the truck.
        velocity (float): Current horizontal velocity (can be positive or negative).
        sprite_to_be_changed_back (bool): Flag to change the truck sprite.
        has_returned (bool): True if the truck has returned to its original position.
        has_turned (bool): True if the truck has turned around off-screen.
    """

    def __init__(self, x: int, y: int, length: int, height: int) -> None:
        """Initializes the truck with position and size.

        :param x: int, initial x coordinate, must be >= 0.
        :param y: int, initial y coordinate, must be >= 0.
        :param length: int, width of the truck, must be > 0.
        :param height: int, height of the truck, must be > 0.
        """
        super().__init__(x, y, length, height)
        self.packages: list[Package] = []
        self.velocity = 1.0
        self.sprite_to_be_changed_back = False
        self.has_returned = False
        self.has_turned = False

    @property
    def velocity(self) -> float:
        """Returns the current horizontal velocity of the truck.

        :return: float, the velocity (can be positive or negative).
        """
        return self.__velocity

    @velocity.setter
    def velocity(self, velocity: float) -> None:
        """Sets the horizontal velocity of the truck.

        :param velocity: float, the new velocity.
        :raises TypeError: if velocity is not numeric.
        """
        if not isinstance(velocity, (int, float)):
            raise TypeError("velocity must be a number (int or float)")
        self.__velocity = float(velocity)

    @property
    def sprite_to_be_changed_back(self) -> bool:
        """Returns whether the truck sprite should be changed back.

        :return: bool, True if the sprite should be reverted.
        """
        return self.__sprite_to_be_changed_back

    @sprite_to_be_changed_back.setter
    def sprite_to_be_changed_back(self, sprite_to_be_changed_back: bool) -> None:
        """Sets whether the truck sprite should be changed back.

        :param sprite_to_be_changed_back: bool, True if the sprite should be reverted.
        :raises TypeError: if sprite_to_be_changed_back is not a bool.
        """
        if not isinstance(sprite_to_be_changed_back, bool):
            raise TypeError("sprite_to_be_changed_back must be a bool")
        self.__sprite_to_be_changed_back = sprite_to_be_changed_back

    @property
    def has_returned(self) -> bool:
        """Returns whether the truck has returned to its original position.

        :return: bool, True if it has returned.
        """
        return self.__has_returned

    @has_returned.setter
    def has_returned(self, has_returned: bool) -> None:
        """Sets whether the truck has returned to its original position.

        :param has_returned: bool, True if it has returned.
        :raises TypeError: if has_returned is not a bool.
        """
        if not isinstance(has_returned, bool):
            raise TypeError("has_returned must be a bool")
        self.__has_returned = has_returned

    @property
    def has_turned(self) -> bool:
        """Returns whether the truck has turned off-screen.

        :return: bool, True if it has turned around.
        """
        return self.__has_turned

    @has_turned.setter
    def has_turned(self, has_turned: bool) -> None:
        """Sets whether the truck has turned off-screen.

        :param has_turned: bool, True if it has turned.
        :raises TypeError: if has_turned is not a bool.
        """
        if not isinstance(has_turned, bool):
            raise TypeError("has_turned must be a bool")
        self.__has_turned = has_turned

    def put_package(self, package: Package) -> None:
        """Loads a package onto the truck bed and marks it delivered.

        The package's state is set to :class:`PackageState.ON_TRUCK` and its
        position is updated to the next free slot on the truck.

        :param package: Package, the package to load.
        :raises TypeError: if package is not a Package instance.
        """
        if not isinstance(package, Package):
            raise TypeError("package must be a Package instance")

        package.state = PackageState.ON_TRUCK
        package.x = self.x + 13 + (package.length * (len(self.packages) // 3))
        package.y = self.y + 14 - (package.height * (len(self.packages) % 3))
        self.packages.append(package)

    def is_full(self) -> bool:
        """Checks whether the truck is full.

        :return: bool, True when the truck has received all required packages.
        """
        return len(self.packages) >= 8

    def truck_in_movement(self, original_x: int) -> None:
        """Animates the truck leaving the screen and returning.

        :param original_x: int, original x position to which the truck must return.
        """
        if not self.has_returned and self.x + self.length + 5 <= 0:
            self.velocity = 0.5
            self.has_turned = True
        elif not self.has_returned and not self.has_turned:
            self.velocity = -1

        if self.x + int(4 * self.velocity) <= original_x:
            self.x += int(4 * self.velocity)
        elif self.x != original_x and self.x + int(4 * self.velocity) > original_x:
            self.x = original_x

        if original_x == self.x:
            self.has_returned = True
            self.has_turned = False
