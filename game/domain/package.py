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

class PackageStage(Enum):
    """Possible life-cycle stages for a :class:`Package`. Used for rendering the appropriate sprite.

    Attributes:
        ON_CONVEYOR_0: Package has not yet passed the middle of the first conveyor belt.
        ON_CONVEYOR_1: Package has not yet passed the middle of the second conveyor belt but has passed the first.
        ON_CONVEYOR_2: Package has not yet passed the middle of the third conveyor belt but has passed the second.
        ON_CONVEYOR_3: Package has not yet passed the middle of the forth conveyor belt but has passed the third.
        ON_CONVEYOR_4: Package has not yet passed the middle of the fifth conveyor belt but has passed the forth.
        ON_CONVEYOR_5: Package has  passed the middle of the fifth conveyor belt.
    """

    ON_CONVEYOR_0 = 0
    ON_CONVEYOR_1 = 1
    ON_CONVEYOR_2 = 2
    ON_CONVEYOR_3 = 3
    ON_CONVEYOR_4 = 4
    ON_CONVEYOR_5 = 5

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
        self, x, y, length, height, state: PackageState = PackageState.ON_CONVEYOR, stage: PackageStage = PackageStage.ON_CONVEYOR_0
    ) -> None:
        if not isinstance(state, PackageState):
            raise TypeError("state must be an instance of PackageState")
        if not isinstance(stage, PackageStage):
            raise TypeError("stage must be an instance of PackageStage")
        self.state = state
        self.stage = stage
        super().__init__(x, y, length, height)


class CanRecievePackage(Protocol):
    @abstractmethod
    def put_package(self, package: Package) -> None:
        raise NotImplementedError
