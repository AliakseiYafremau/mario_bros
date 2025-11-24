from game.domain.elements import MotionElement
from game.domain.package import Package, PackageState


class Truck(MotionElement):
    def __init__(self, x, y, length, height) -> None:
        self.packages: list = []
        self.velocity: int = 1
        self.sprite_to_be_changed_back = False
        self.has_returned: bool = False
        self.has_turned: bool = False
        super().__init__(x, y, length, height)

    def put_package(self, package: Package) -> None:
        package.state = PackageState.ON_TRUCK
        package.x = self.x + 13 + ((package.length + 1) * (len(self.packages) // 3))
        package.y = self.y + 14 - ((package.height + 1) * (len(self.packages) % 3))
        self.packages.append(package)

    def is_full(self) -> bool:
        return len(self.packages) >= 1

    def truck_in_movement(self, original_x: int) -> None:
        if not self.has_returned and self.x + self.length + 5 <= 0 :
            self.velocity = 0.5
            self.has_turned = True
        elif not self.has_returned and not self.has_turned:
            self.velocity = -1
        if self.x + int(4*self.velocity) <= original_x:
            self.x += int(4*self.velocity)
        elif self.x != original_x and self.x + int(4*self.velocity) > original_x:
            self.x = original_x
        if original_x == self.x:
            self.has_returned = True
            self.has_turned = False