from game.domain.elements import MotionElement
from game.domain.package import Package, PackageState


class Truck(MotionElement):
    """Movable delivery truck that accepts completed packages."""

    def __init__(self, x, y, length, height) -> None:
        self.packages: list = []
        self.velocity: float = 1
        self.sprite_to_be_changed_back = False
        self.has_returned: bool = False
        self.has_turned: bool = False
        super().__init__(x, y, length, height)

    def put_package(self, package: Package) -> None:
        """Load a package onto the truck bed and mark it delivered."""
        package.state = PackageState.ON_TRUCK
        package.x = self.x + 13 + (package.length * (len(self.packages) // 3))
        package.y = self.y + 14 - (package.height * (len(self.packages) % 3))
        self.packages.append(package)

    def is_full(self) -> bool:
        """Return True when the truck has received all required packages."""
        return len(self.packages) >= 8

    def truck_in_movement(self, original_x: int) -> None:
        """Animate the truck leaving the screen and returning."""
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
