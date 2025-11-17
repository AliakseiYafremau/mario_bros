from game.domain.conveyor import Conveyor
from game.domain.elements import Element
from game.domain.logging import get_logger
from game.domain.package import Package, PackageState


logger = get_logger(__name__, "DOMAIN")


class PackageFactory(Element):
    """Factory to create Package instances."""

    def __init__(
        self,
        x: int,
        y: int,
        length: int,
        height: int,
        new_package_x: int,
        new_package_y: int,
        new_package_length: int,
        new_package_height: int,
        conveyor: Conveyor,
    ) -> None:
        self.new_package_x = new_package_x
        self.new_package_y = new_package_y
        self.new_package_length = new_package_length
        self.new_package_height = new_package_height
        self.conveyor = conveyor
        super().__init__(x, y, length, height)

    def create_package(self) -> Package:
        package = Package(
            x=self.new_package_x,
            y=self.new_package_y,
            length=self.new_package_length,
            height=self.new_package_height,
            state=PackageState.ON_CONVEYOR,
        )
        self.conveyor.put_package(package)
        logger.debug("%s created package %s", self.__repr__(), package)
        return package
