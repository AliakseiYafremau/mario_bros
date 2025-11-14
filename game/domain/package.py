from enum import Enum
from game.domain.elements import MotionElement


class PackageState(Enum):
    """Possible life-cycle states for a :class:`Package`.

    Attributes:
        ON_CONVEYOR: Package is on a conveyor belt.
        ON_TRUCK: Package is loaded on a truck.
        PICKED: Package has been picked by the player.
        FALLING: Package is in a falling state (not supported by all
            game subsystems).
    """

    ON_CONVEYOR = "conveyor"
    ON_TRUCK = "truck"
    PICKED = "picked"
    FALLING = "falling"


class Package(MotionElement):
    """The movable package in the game world.

    The `Package` is a small value-object representing an item
    that can move along conveyors, be picked by the player, or loaded
    onto trucks.

    Attributes:
        x (int): Current X coordinate.
        y (int): Current Y coordinate.
        weigth (int): Width of the package.
        height (int): Height of the package.
        state (PackageState): Current state of the package.

    Raises:
        TypeError: If ``state`` is not a :class:`PackageState` instance.
    """

    def __init__(
        self, x, y, length, height, state: PackageState = PackageState.ON_CONVEYOR
    ) -> None:
        if not isinstance(state, PackageState):
            raise TypeError("state must be an instance of PackageState")
        self.state = state
        super().__init__(x, y, length, height)
