from struct import pack
from tkinter import Pack
from game.domain.directions import Direction
from game.domain.elements import Element
from game.domain.package import Package

class Conveyor(Element):
    def __init__(self, x: int, y: int, length: int, height: int, direction: Direction, velocity: int):
        self.direction = direction
        self.velocity = velocity
        self._packages: list[Package] = []
        super().__init__(x, y, length, height)

    def move_packages(self):
        for package in self._packages:
            package.move_x(self._velocity)
            if not self._is_package_on_conveyor(package):
                self.lift_package(package)
    
    def put_package(self, package: Package):
        if not isinstance(package, Package):
            raise TypeError("package must be a Package instance")
        package.is_on_conveyor = True
        self._packages.append(package)
    
    def lift_package(self, package: Package):
        self._packages.remove(package)
        package.is_on_conveyor = False

    def _is_package_on_conveyor(self, package: Package) -> bool:
        if self.x + self.length < package.x:
            return False
        return True

    @property
    def velocity(self):
        return self._velocity
    
    @property
    def direction(self):
        return self._direction
    
    @velocity.setter
    def velocity(self, value):
        if value < 0:
            raise ValueError("Velocity cannot be negative")
        self._velocity = value

    @direction.setter
    def direction(self, value):
        if not isinstance(value, Direction):
            raise TypeError("direction must be a Direction instance")
        self._direction = value