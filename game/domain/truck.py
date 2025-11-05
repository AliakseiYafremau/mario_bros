from game.domain.elements import MotionElement
from game.domain.package import Package, PackageState


class Truck(MotionElement):
    def __init__(self, x, y, length, height):
        self._packages: list[Package] = []
        super().__init__(x, y, length, height)

    def put_package(self, package: Package) -> None:
        if not isinstance(package, Package):
            raise TypeError("package must be a Package instance")
        package.state = PackageState.ON_TRUCK
        self._packages.append(package)

    def is_full(self) -> bool:
        return len(self._packages) >= 8
