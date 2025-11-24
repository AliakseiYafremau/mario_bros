from game.domain.elements import MotionElement
from game.domain.package import Package, PackageState


class Truck(MotionElement):
    def __init__(self, x, y, length, height) -> None:
        self.packages: list = []
        super().__init__(x, y, length, height)

    def put_package(self, package: Package) -> None:
        package.state = PackageState.ON_TRUCK
        package.x = self.x + 13 + ((package.length + 1) * (len(self.packages) // 3))
        package.y = self.y + 14 - ((package.height + 1) * (len(self.packages) % 3))
        self.packages.append(package)

    def is_full(self) -> bool:
        return len(self.packages) >= 8

    def truck_leaves(self) -> None:
        self.packages = []
