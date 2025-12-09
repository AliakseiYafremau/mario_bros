from abc import abstractmethod
from enum import Enum
from typing import Protocol

from game.domain.elements import MotionElement


class PackageState(Enum):
    """Possible life-cycle positions for a :class:`Package`.

    Attributes:
        ON_CONVEYOR: Package is on a conveyor belt.
        PICKED: Package has been picked by the player.
        FALLING: Package is in a falling state (not supported by all subsystems).
        ON_TRUCK: Package has been successfully loaded onto the truck.
    """

    ON_CONVEYOR = "conveyor"
    PICKED = "picked"
    FALLING = "falling"
    ON_TRUCK = "truck"


class Package(MotionElement):
    """The movable package in the game world.

    The `Package` is a small value-object representing an item
    that can move along conveyors, be picked by the player, or loaded
    onto trucks.

    Attributes:
        x (int): Current x coordinate (non-negative).
        y (int): Current y coordinate (non-negative).
        length (int): Width of the package (positive).
        height (int): Height of the package (positive).
        state (PackageState): Current state of the package.
        stage (int): Stage of the package in the pipeline, between 0 and 5 inclusive.
        stage_to_be_changed_to (int): Pending stage change (0 means no change).
        state_to_be_changed_to (int): Pending state change (0 = none, 1 = falls left, 2 = falls right).
        offscreen (bool): True if the package is outside the visible area.
    """

    def __init__(
        self,
        x: int,
        y: int,
        length: int,
        height: int,
        state: PackageState = PackageState.ON_CONVEYOR,
        stage: int = 0,
    ) -> None:
        """Initializes a package with position, size, state and stage.

        :param x: int, initial x coordinate, must be >= 0.
        :param y: int, initial y coordinate, must be >= 0.
        :param length: int, width of the package, must be > 0.
        :param height: int, height of the package, must be > 0.
        :param state: PackageState, initial life-cycle state of the package.
        :param stage: int, initial stage (0 to 5 inclusive).
        :raises TypeError: if state is not a PackageState or stage has wrong type.
        :raises ValueError: if stage is not between 0 and 5.
        """
        super().__init__(x, y, length, height)
        self.state = state
        self.stage = stage
        self.stage_to_be_changed_to = 0
        self.state_to_be_changed_to = 0
        self.offscreen = False

    # state
    @property
    def state(self) -> PackageState:
        """Returns the current state of the package.

        :return: PackageState, the current package state.
        """
        return self.__state

    @state.setter
    def state(self, state: PackageState) -> None:
        """Sets the current state of the package.

        :param state: PackageState, the new state.
        :raises TypeError: if state is not a PackageState instance.
        """
        if not isinstance(state, PackageState):
            raise TypeError("state must be an instance of PackageState")
        self.__state = state

    # stage
    @property
    def stage(self) -> int:
        """Returns the current stage of the package.

        :return: int, the stage number between 0 and 5 inclusive.
        """
        return self.__stage

    @stage.setter
    def stage(self, stage: int) -> None:
        """Sets the current stage of the package.

        :param stage: int, the new stage, must be between 0 and 5 inclusive.
        :raises TypeError: if stage is not an int.
        :raises ValueError: if stage is not in range 0..5.
        """
        if not isinstance(stage, int):
            raise TypeError("stage must be an int")
        if not 0 <= stage <= 5:
            raise ValueError("stage must be between 0 and 5 inclusive")
        self.__stage = stage

    # stage_to_be_changed_to
    @property
    def stage_to_be_changed_to(self) -> int:
        """Returns the pending stage change.

        :return: int, 0 means no change; otherwise the new stage (0..5).
        """
        return self.__stage_to_be_changed_to

    @stage_to_be_changed_to.setter
    def stage_to_be_changed_to(self, stage: int) -> None:
        """Sets the pending stage change.

        :param stage: int, 0 means no change; otherwise new stage (0..5).
        :raises TypeError: if stage is not an int.
        :raises ValueError: if stage is not between 0 and 5 inclusive.
        """
        if not isinstance(stage, int):
            raise TypeError("stage_to_be_changed_to must be an int")
        if not 0 <= stage <= 5:
            raise ValueError("stage_to_be_changed_to must be between 0 and 5 inclusive")
        self.__stage_to_be_changed_to = stage

    # state_to_be_changed_to
    @property
    def state_to_be_changed_to(self) -> int:
        """Returns the pending state change flag.

        :return: int, 0 = no change, 1 = falls to the left, 2 = falls to the right.
        """
        return self.__state_to_be_changed_to

    @state_to_be_changed_to.setter
    def state_to_be_changed_to(self, value: int) -> None:
        """Sets the pending state change flag.

        :param value: int, 0 = none, 1 = falls to the left, 2 = falls to the right.
        :raises TypeError: if value is not an int.
        :raises ValueError: if value is not 0, 1 or 2.
        """
        if not isinstance(value, int):
            raise TypeError("state_to_be_changed_to must be an int")
        if value not in (0, 1, 2):
            raise ValueError("state_to_be_changed_to must be 0, 1 or 2")
        self.__state_to_be_changed_to = value

    # offscreen
    @property
    def offscreen(self) -> bool:
        """Returns whether the package is offscreen.

        :return: bool, True if the package is outside the visible area.
        """
        return self.__offscreen

    @offscreen.setter
    def offscreen(self, offscreen: bool) -> None:
        """Sets whether the package is offscreen.

        :param offscreen: bool, True if the package is outside the visible area.
        :raises TypeError: if offscreen is not a bool.
        """
        if not isinstance(offscreen, bool):
            raise TypeError("offscreen must be a bool")
        self.__offscreen = offscreen


class CanRecievePackage(Protocol):
    """Protocol describing any object that can receive packages.

    Any class implementing this protocol must provide a method:

        put_package(self, package: Package) -> None
    """

    @abstractmethod
    def put_package(self, package: Package) -> None:
        """Receives a package.

        :param package: Package, the package to be received.
        :raises NotImplementedError: if not implemented in subclasses.
        """
        raise NotImplementedError
