from game.domain.elements import MotionElement
from game.domain.exceptions import DomainError
from game.domain.package import Package, PackageState


class Player(MotionElement):
    """The player character in the game world.

    The `Player` is a controllable character that can move around
    the game world, pick up `Package` objects, and interact with other
    game elements.

    Attributes:
        x (int): Current X coordinate.
        y (int): Current Y coordinate.
        length (int): Length of the player in the X axis.
        height (int): Height of the player in the Y axis.
        name (str): Name of the player.
        package (Package | None): The package currently held by the player,
            or None if no package is held.

    Raises:
        TypeError: If ``package`` is not a :class:`Package` instance or None.
    """

    def __init__(self, x, y, length, height, name) -> None:
        self.name = name
        self._package: Package | None = None
        super().__init__(x, y, length, height)

    @property
    def package(self) -> Package | None:
        return self._package

    @package.setter
    def package(self, value):
        if not isinstance(value, Package) or (value is not None):
            raise TypeError("package must be a Package instance or None")
        self._package = value

    def pick_package(self, package: Package) -> None:
        if self.package is not None:
            raise DomainError("player already has a package")
        package.state = PackageState.PICKED
        self.package = package

    def put_package(self) -> None:
        if self.package is None:
            raise DomainError("player does not have any package")
        self.package.state = PackageState.FALLING
        self.package = None

    def move(self, x=0, y=0) -> None:
        if self.package is not None:
            self.package.move(x=x, y=y)
        return super().move(x, y)

    def move_x(self, x) -> None:
        return self.move(x=x, y=0)

    def move_y(self, y) -> None:
        return self.move(x=0, y=y)
