from time import perf_counter

from game.domain.elements import MotionElement
from game.domain.exceptions import DomainError
from game.domain.package import Package, PackageState


class Player(MotionElement):
    """The player characters.

    The `Player` is a controllable character that can move around
    , pick up :class:`Package` objects, and interact with other
    game elements.

    Attributes:
        x (int): Current x coordinate (non-negative).
        y (int): Current y coordinate (non-negative).
        length (int): Length of the player in the x axis (positive).
        height (int): Height of the player in the y axis (positive).
        name (str): Name of the player (non-empty).
        package (Package | None): Currently held package, if any.
        is_moving_package (bool): True if the player is currently moving a package.
        package_picked_up_at (float): Time stamp when the current package was picked up.
        sprite_to_be_changed (bool): True if the player's sprite needs to be updated.
        on_the_factory_level (bool): True if the player is in the factory floor.
        is_resting (bool): True if the player is currently resting after a delivery.
    """

    def __init__(self, x: int, y: int, length: int, height: int, name: str) -> None:
        """Initializes the player with position, size and name.

        :param x: int, initial x coordinate (must be >= 0).
        :param y: int, initial y coordinate (must be >= 0).
        :param length: int, width of the player (must be > 0).
        :param height: int, height of the player (must be > 0).
        :param name: str, name of the player (non-empty).
        :raises TypeError: if types are not correct.
        :raises ValueError: if name is empty or sizes are invalid (from parent).
        """
        super().__init__(x, y, length, height)
        self.name = name
        self.package = None
        self.is_moving_package = False
        self.package_picked_up_at = 0.0
        self.sprite_to_be_changed = False
        self.on_the_factory_level = False
        self.is_resting = False

    @property
    def name(self) -> str:
        """Returns the name of the player.

        :return: str, the player's name.
        """
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        """Sets the name of the player.

        :param name: str, the new name (must be non-empty).
        :raises TypeError: if name is not a string.
        :raises ValueError: if name is empty.
        """
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if name.strip() == "":
            raise ValueError("name cannot be empty")
        self.__name = name

    @property
    def package(self) -> Package | None:
        """Returns the package currently held by the player.

        :return: Package or None, the current package.
        """
        return self.__package

    @package.setter
    def package(self, package: Package | None) -> None:
        """Sets the package currently held by the player.

        :param package: Package or None, the package to hold.
        :raises TypeError: if package is not a Package or None.
        """
        if package is not None and not isinstance(package, Package):
            raise TypeError("package must be a Package instance or None")
        self.__package = package

    @property
    def is_moving_package(self) -> bool:
        """Returns whether the player is currently moving a package.

        :return: bool, True if moving a package.
        """
        return self.__is_moving_package

    @is_moving_package.setter
    def is_moving_package(self, is_moving_package: bool) -> None:
        """Sets whether the player is currently moving a package.

        :param is_moving_package: bool, True if moving a package.
        :raises TypeError: if is_moving_package is not a bool.
        """
        if not isinstance(is_moving_package, bool):
            raise TypeError("is_moving_package must be a bool")
        self.__is_moving_package = is_moving_package

    @property
    def package_picked_up_at(self) -> float:
        """Returns the time when the current package was picked up.

        :return: float, the time stamp (seconds).
        """
        return self.__package_picked_up_at

    @package_picked_up_at.setter
    def package_picked_up_at(self, package_picked_up_at: float) -> None:
        """Sets the time when the current package was picked up.

        :param package_picked_up_at: float, time stamp in seconds.
        :raises TypeError: if package_picked_up_at is not a number.
        """
        if not isinstance(package_picked_up_at, (int, float)):
            raise TypeError("package_picked_up_at must be a number")
        self.__package_picked_up_at = float(package_picked_up_at)

    @property
    def sprite_to_be_changed(self) -> bool:
        """Returns whether the player's sprite should be changed.

        :return: bool, True if the sprite should be changed.
        """
        return self.__sprite_to_be_changed

    @sprite_to_be_changed.setter
    def sprite_to_be_changed(self, sprite_to_be_changed: bool) -> None:
        """Sets whether the player's sprite should be changed.

        :param sprite_to_be_changed: bool, True if the sprite should be changed.
        :raises TypeError: if sprite_to_be_changed is not a bool.
        """
        if not isinstance(sprite_to_be_changed, bool):
            raise TypeError("sprite_to_be_changed must be a bool")
        self.__sprite_to_be_changed = sprite_to_be_changed

    @property
    def on_the_factory_level(self) -> bool:
        """Returns whether the player is on the factory level.

        :return: bool, True if on the factory level.
        """
        return self.__on_the_factory_level

    @on_the_factory_level.setter
    def on_the_factory_level(self, on_the_factory_level: bool) -> None:
        """Sets whether the player is on the factory level.

        :param on_the_factory_level: bool, True if on the factory level.
        :raises TypeError: if on_the_factory_level is not a bool.
        """
        if not isinstance(on_the_factory_level, bool):
            raise TypeError("on_the_factory_level must be a bool")
        self.__on_the_factory_level = on_the_factory_level

    @property
    def is_resting(self) -> bool:
        """Returns whether the player is resting.

        :return: bool, True if resting.
        """
        return self.__is_resting

    @is_resting.setter
    def is_resting(self, is_resting: bool) -> None:
        """Sets whether the player is resting.

        :param is_resting: bool, True if resting.
        :raises TypeError: if is_resting is not a bool.
        """
        if not isinstance(is_resting, bool):
            raise TypeError("is_resting must be a bool")
        self.__is_resting = is_resting

    def pick_package(self, package: Package) -> bool:
        """Makes the player pick up a package if none is currently held.

        The package is centered inside the player's bounding box and its state
        is set to :class:`PackageState.PICKED`.

        :param package: Package, the package to be picked up.
        :return: bool, True if the package was picked up, False if the player already had one.
        """
        if self.package is not None:
            return False

        package.state = PackageState.PICKED
        package.x = self.x + ((self.length - package.length) // 2)
        package.y = self.y + ((self.height - package.height) // 2)
        self.package = package
        self.is_moving_package = True
        self.package_picked_up_at = perf_counter()
        return True

    def put_package(self) -> None:
        """Makes the player put down the currently held package.

        After calling this method the player no longer carries any package.

        :raises DomainError: if the player does not have any package.
        """
        if self.package is None:
            raise DomainError("player does not have any package")
        self.package = None

    def move(self, x: int = 0, y: int = 0) -> None:
        """Moves the player to a new position.

        If the player is carrying a package, the package is moved together
        to the same coordinates.

        :param x: int, new x coordinate (must be >= 0).
        :param y: int, new y coordinate (must be >= 0).
        """
        if self.package is not None:
            self.package.move(x=x, y=y)
        super().move(x, y)

    def move_x(self, x: int) -> None:
        """Moves the player horizontally.

        :param x: int, new x coordinate (must be >= 0).
        """
        self.move(x=x, y=self.y)

    def move_y(self, y: int) -> None:
        """Moves the player vertically.

        :param y: int, new y coordinate (must be >= 0).
        """
        self.move(x=self.x, y=y)
