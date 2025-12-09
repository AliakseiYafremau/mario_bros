from game.domain.conveyor import Conveyor
from game.domain.elements import Element
from game.domain.package import Package, PackageState


class PackageFactory(Element):
    """Factory to create :class:`Package` instances.

    Attributes:
        x (int): x-coordinate of the factory (non-negative).
        y (int): y-coordinate of the factory (non-negative).
        length (int): width of the factory (positive).
        height (int): height of the factory (positive).
        new_package_length (int): width of new packages (positive).
        new_package_height (int): height of new packages (positive).
        conveyor (Conveyor): conveyor on which new packages are placed.
    """

    def __init__(
        self,
        x: int,
        y: int,
        length: int,
        height: int,
        new_package_length: int,
        new_package_height: int,
        conveyor: Conveyor,
    ) -> None:
        """Initializes the package factory.

        :param x: int, x-coordinate of the factory (must be >= 0).
        :param y: int, y-coordinate of the factory (must be >= 0).
        :param length: int, width of the factory (must be > 0).
        :param height: int, height of the factory (must be > 0).
        :param new_package_length: int, width of new packages (must be > 0).
        :param new_package_height: int, height of new packages (must be > 0).
        :param conveyor: Conveyor, conveyor where new packages will be placed.
        :raises TypeError: if any parameter has an incorrect type.
        :raises ValueError: if any size is not positive.
        """
        super().__init__(x, y, length, height)
        self.new_package_length = new_package_length
        self.new_package_height = new_package_height
        self.conveyor = conveyor

    @property
    def new_package_length(self) -> int:
        """Returns the width of newly created packages.

        :return: int, the package length (positive).
        """
        return self.__new_package_length

    @new_package_length.setter
    def new_package_length(self, new_package_length: int) -> None:
        """Sets the width of newly created packages.

        :param new_package_length: int, width of new packages (must be > 0).
        :raises TypeError: if new_package_length is not an int.
        :raises ValueError: if new_package_length is not positive.
        """
        if not isinstance(new_package_length, int):
            raise TypeError("new_package_length must be an int")
        if new_package_length <= 0:
            raise ValueError("new_package_length must be positive")
        self.__new_package_length = new_package_length

    @property
    def new_package_height(self) -> int:
        """Returns the height of newly created packages.

        :return: int, the package height (positive).
        """
        return self.__new_package_height

    @new_package_height.setter
    def new_package_height(self, new_package_height: int) -> None:
        """Sets the height of newly created packages.

        :param new_package_height: int, height of new packages (must be > 0).
        :raises TypeError: if new_package_height is not an int.
        :raises ValueError: if new_package_height is not positive.
        """
        if not isinstance(new_package_height, int):
            raise TypeError("new_package_height must be an int")
        if new_package_height <= 0:
            raise ValueError("new_package_height must be positive")
        self.__new_package_height = new_package_height

    @property
    def conveyor(self) -> Conveyor:
        """Returns the conveyor associated with this factory.

        :return: Conveyor, the conveyor used to place new packages.
        """
        return self.__conveyor

    @conveyor.setter
    def conveyor(self, conveyor: Conveyor) -> None:
        """Sets the conveyor associated with this factory.

        :param conveyor: Conveyor, the conveyor used to place new packages.
        :raises TypeError: if conveyor is not a Conveyor instance.
        """
        if not isinstance(conveyor, Conveyor):
            raise TypeError("conveyor must be a Conveyor instance")
        self.__conveyor = conveyor

    def create_package(self) -> Package:
        """Creates a new package and places it on the associated conveyor.

        The (x, y) position is initially set to 0, 0 because it will be
        overridden by :meth:`Conveyor.put_package`.

        :return: Package, the newly created package.
        """
        package = Package(
            x=0,
            y=0,
            length=self.new_package_length,
            height=self.new_package_height,
            state=PackageState.ON_CONVEYOR,
            stage=0,
        )
        self.conveyor.put_package(package)
        return package
