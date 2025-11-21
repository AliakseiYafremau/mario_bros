from abc import ABC, abstractmethod
from enum import Enum
from typing import Protocol
from game.domain.elements import MotionElement


class PackageState(Enum):
    """Possible life-cycle positions for a :class:`Package`.

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
        stage (PackageStage): Current stage of the package.

    Raises:
        TypeError: If ``state`` is not a :class:`PackageState` instance.
    """

    def __init__(
        self, x, y, length, height, state: PackageState = PackageState.ON_CONVEYOR, stage: int = 0
    ) -> None:
        if not isinstance(state, PackageState):
            raise TypeError("state must be an instance of PackageState")
        if not isinstance(stage, int) or not (0 <= stage <= 5):
            raise TypeError("stage must be an instance of int and between 0 and 5 inclusive")
        self.state = state
        self.stage = stage
        self.stage_to_be_changed_to = 0 # 0 means no change but a value diffrent form 0 means it gets changed to that respective stage
        self.state_to_be_changed_to = 0 # 0 means no change, 1 means it falls to the left, 2 means it falls to the right
        self.offscreen = False
        super().__init__(x, y, length, height)


class CanRecievePackage(Protocol):
    @abstractmethod
    def put_package(self, package: Package) -> None:
        raise NotImplementedError
