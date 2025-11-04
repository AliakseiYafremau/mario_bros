from enum import Enum
from game.domain.elements import MotionElement


class PackageState(Enum):
    ON_CONVEYOR = "conveyor"
    ON_TRUCK = "truck"
    PICKED = "picked"
    FALLING = "falling"


class Package(MotionElement):
    def __init__(self, x, y, length, height):
        self.state: PackageState = PackageState.ON_CONVEYOR
        super().__init__(x, y, length, height)