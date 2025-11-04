from game.domain.elements import MotionElement
from game.domain.package import Package


class Truck(MotionElement):
    def __init__(self, x, y, length, height):
        self._packages: list[Package] = []
        super().__init__(x, y, length, height)
    
    def put_package(self, package: Package):
        if not isinstance(package, Package):
            raise TypeError("package must be a Package instance")
        package.is_on_conveyor = True
        self._packages.append(package)