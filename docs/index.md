# Summary

Mario Bros is a  conveyor-warehouse challenge: Luigi and Mario shuffle along multi-level belts, catching fragile packages, tossing them across gaps, and passing them down the line so every crate survives the trip to the truck. The game mixes timing puzzles with light platforming—ride lifts, flip switches, clear jams, and keep both plumbers in sync to stop packages from crashing before they reach the loading dock.

# Classes

## Main logic

### Element
`Element` is the immutable geometric base for everything placed into the world. It stores the axis-aligned bounding box (`x`, `y`, `length`, `height`).

```python
class Element:
  def __init__(self, x: int, y: int, length: int, height: int) -> None:
    ...
```

### MotionElement
`Element`, with implementation of methods allowing it to move in the world.

```python
class MotionElement(Element):
  def move(self, x: int = 0, y: int = 0) -> None:
    """Moves the object along the x and y axes."""

  def move_x(self, x: int) -> None:
    """Moves the object along the x axis."""

  def move_y(self, y: int) -> None:
    """Moves the object along the y axis."""
```

### Player
`Player` it is movable object that models Luigi or Mario. A player can either pick or put his package. He cannot take the package if he already has one, or put it down if he does not have one.

```python
class Player(MotionElement):
  def __init__(self, x, y, length, height, name) -> None:
    ...

  def pick_package(self, package: Package) -> None:
    """Pick package if it does not have it."""

  def put_package(self) -> None:
    """Put package if it has it"""
```

### Package
`Package` is the physical crate (`Element`) that rides conveyors. Has several states: `ON_CONVEYOR`, `PICKED`, `FALLING`, and `ON_TRUCK`.

### Conveyor
`Conveyor` defines each belt span in the warehouse and specifies which way crates travel, how fast they ride, and where they should land next. By tracking the active package queue, its `finish_floor`, and the downstream `next_conveyor`, it is the component that hands cargo off from one work station to another.
Key attributes: `direction` (left or right travel), `velocity` (tiles per tick), `_packages` (queue of packages currently on the belt), `finish_floor` (the floor that receives falling crates), `next_conveyor` (where a caught package continues), and `falling_package` (the crate currently leaving the belt).

### PackageFactory
`PackageFactory` represents the loading dock that injects new crates into the system. It stores the spawn coordinates for packages and, on demand, produces a ready-to-ride `Package` that joins its assigned conveyor without player intervention.
Key attributes: `new_package_x`, `new_package_y`, `new_package_length`, `new_package_height` (spawn geometry), and `conveyor` (the belt that immediately receives the new package).

### Floor
`Floor` names the individual platforms where plumbers can stand during the shift. It pairs fixed coordinates with whichever `Player` is stationed there so the game can reason about legal elevator stops and enforce that tasks happen from the correct level.
Key attributes: `x`, `y` (platform position), and `player` (the plumber currently working that station).

### Truck
`Truck` is the delivery target: a movable cargo bay that accepts completed packages and counts toward the win condition. When its hold reaches eight crates the round is done.
Key attributes: `capacity` (always eight), `cargo` (list of delivered packages), and inherited `x`, `y`, `length`, `height` defining the bay.

### Game
`Game` is the supervisor for the entire shift: it knows all players, belts, factories, and the truck, ensures plumbers stand on valid floors, tracks the remaining lives, and exposes the actions—moving packages, spawning crates, or relocating a player—that keep the level running. Think of it as the facade that bundles the simulation API behind one object so callers have a single entry point for advancing the level.
Key attributes: `players` (tuple of controllable characters), `floors` (allowed positions for each player), `conveyors`, `factories`, `truck`, `tick` (global time), and `live_amount` (remaining lives before game over).

## Pyxel util classes

### Controller
Command class that facilitates handling user input by providing a unified interface for each function.

```python
class Controller:
  def execute(self):
    ...
```

### PyxelElement

Class that renders an object in the application based on game elements and frames data.

`PyxelStaticElement` is used for the same purpose, but it does not need an object to display. Accordingly, it is __static__. It is used for stage decorations.

`Frame` stores information about images. It is used to display several photos for one element at once (since an element can be complex and consist of more than one image (for example, a conveyor belt)).

### BoardedPyxelElement
Decorator for any `PyxelElement` that draws a rectangular border sized after the element's `length` and `height` (plus optional padding) before delegating to the wrapped element's `draw()`. It is intended as a _development_ aid when you need to highlight, align, or debug sprites during Pyxel scene tuning.

### PyxelApp
`PyxelApp` wires the Pyxel event loop to the game simulation: it loads sprite resources, keeps a list of `PyxelElement` instances to draw, binds `Controller`s to keyboard buttons, and advances `Game` ticks according to configurable delays for package movement and creation. On every update it polls the buttons, extends the render list with freshly spawned packages, and calls `Game.move_packages()` / `Game.create_package()` when the elapsed time exceeds the configured cadence before redrawing the scene.

# Main Algorithms
## `Game.move_packages()` 
It is the heart of the loop. First, it inspects every `Conveyor` for a `falling_package`. If the target `finish_floor` hosts a `Player`, the player briefly picks that package, drops it toward the `next_conveyor`, and the controller inserts it onto the next belt; otherwise a dropped package decrements `live_amount`. After resolving transfers it calls `Conveyor.move_packages()` on each belt and increments the global `tick`.
## `Conveyor.move_packages()`
It iterates through its `_packages`, offsets each package horizontally by `velocity` toward `direction`, and checks `_is_package_on_conveyor()`. Packages that have moved beyond the physical span are marked `FALLING`, recorded as `falling_package`, and removed via `lift_package()` so they can be caught by the next floor.
## `Game.move_player_up()` / `move_player_down()`
They take a `Player`, find their current `Floor` within the allowed tuple, and move exactly one step toward the target tier. They guard against moving past the ends of the tuple and raise a `DomainError` if a player's coordinates no longer match any known floor.
## `Game.create_package()`
It asks every `PackageFactory` to `create_package()`, which in turn spawns a `Package` at the configured coordinates and places it on a belt so it joins the next simulation step automatically.
## `Truck.put_package()`It is the terminal sink: whenever an external actor loads a package on the truck, it flips the package state to `ON_TRUCK` and enforces the eight-package capacity via `is_full()`.
## Tick (PyxelApp.tick_second)
To emulate the movement of older consoles, the concept of ticks was implemented. The number of ticks per second indicates the number of updates that will be made in one second. This allows us to not depend on the player's FPS (which could be the case if we used `pyxel.update()` directly).

To facilitate development and increase scalability, the project's business logic was moved to the domain and separated from the libraries.

A class with corresponding methods was created for each entity in the game. The _player_ represents the movable player in the game. The _conveyor_ is responsible for moving _packages_, and the _package factory_ is responsible for creating them.

To facilitate working with the _domain_ API, a `Game` facade was created, which includes the basic methods for working with the game.

Since the [`pyxel`](https://github.com/kitao/pyxel) library only provides basic display functionality, several secondary classes were created to facilitate working with the library. `Controller` is a command pattern that provides a unified interface for all user input. `PyxelElement` allows you to create complex elements from multiple images (`Frames`).