from enum import Enum
from game.domain.elements import MotionElement


class PackageState(Enum):
    ON_CONVEYOR = "conveyor"
    ON_TRUCK = "truck"
    PICKED = "picked"
    FALLING = "falling"
    FREE = "free"


class Package(MotionElement):
    def __init__(
        self, x, y, length, height, state: PackageState = PackageState.ON_CONVEYOR
    ):
        self.state = state
        super().__init__(x, y, length, height)
