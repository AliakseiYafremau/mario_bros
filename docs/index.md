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

### PackageState
`PackageState` is the enum that records the life-cycle of a crate. The four values—`ON_CONVEYOR`, `PICKED`, `FALLING`, and `ON_TRUCK`—drive which subsystem may act on the package and which sprite frame should be rendered.

### Conveyor
`Conveyor` defines each belt span in the warehouse and specifies which way crates travel, how fast they ride, and where they should land next. By tracking the active package queue, its `finish_floor`, and the downstream `next_conveyor`, it is the component that hands cargo off from one work station to another.
Key attributes: `direction` (left or right travel), `velocity` (tiles per tick), `_packages` (queue of packages currently on the belt), `finish_floor` (the floor that receives falling crates), `next_conveyor` (where a caught package continues), and `falling_package` (the crate currently leaving the belt).

### Direction
`Direction` is the left/right enum used by conveyors. It tells `Conveyor.move_packages()` which edge is the entry point and which direction to offset package coordinates.

### PackageFactory
`PackageFactory` represents the loading dock that injects new crates into the system. It stores the spawn coordinates for packages and, on demand, produces a ready-to-ride `Package` that joins its assigned conveyor without player intervention.
Key attributes: `new_package_x`, `new_package_y`, `new_package_length`, `new_package_height` (spawn geometry), and `conveyor` (the belt that immediately receives the new package).

### Floor
`Floor` names the individual platforms where plumbers can stand during the shift. It pairs fixed coordinates with whichever `Player` is stationed there so the game can reason about legal elevator stops and enforce that tasks happen from the correct level.
Key attributes: `x`, `y` (platform position), and `player` (the plumber currently working that station).

### DomainError
`DomainError` is the custom exception raised when a game rule is violated (moving beyond available floors, picking a package illegally, etc.). Controllers swallow it so invalid inputs simply have no effect instead of crashing the loop.

### Truck
`Truck` is the delivery target: a movable cargo bay that accepts completed packages and counts toward the win condition. When its hold reaches eight crates the round is done.
Key attributes: `capacity` (always eight), `cargo` (list of delivered packages), and inherited `x`, `y`, `length`, `height` defining the bay.

### Game
`Game` is the supervisor for the entire shift: it knows all players, belts, factories, and the truck, ensures plumbers stand on valid floors, tracks the remaining lives, and exposes the actions—moving packages, spawning crates, or relocating a player—that keep the level running. Think of it as the facade that bundles the simulation API behind one object so callers have a single entry point for advancing the level.
Key attributes: `players` (tuple of controllable characters), `floors` (allowed positions for each player), `conveyors`, `factories`, `truck`, `tick` (global time), and `live_amount` (remaining lives before game over).

### Boss
`Boss` is the surprise inspector that occasionally visits to penalize sloppy play. It inherits `Element` for positioning and carries two extra flags: `comes_in_time`, the timestamp when the boss entered through the door, and `has_to_leave`, which signals the rendering layer to remove the sprite after the visit ends.

### Door
`Door` is the portal the `Boss` uses. It extends `Element` with a direct reference to the associated `Boss`, letting the presentation layer spawn or hide the inspector based on door animation frames and visit timing.

### Difficulty
`Difficulty` centralizes the scaling presets. It stores the active difficulty index and exposes `difficulty_values()`, which returns a dictionary describing belts per map, conveyor speeds, point thresholds for increasing difficulty, extra-life cadence, control inversion, and window bounds. Both the game setup and Pyxel windows read from this mapping to stay in sync.

## Pyxel util classes

### Screen
`Screen` is the abstract base for every Pyxel screen. It only stores a reference to the owning `App` and defines the `update()`/`draw()` interface, which `DifficultySelectorScreen`, `GameApp`, and `GameOverScreen` implement.

### App
`App` is the Pyxel bootstrapper. It looks at the command-line arguments to decide which screen to display (difficulty selector, running game, or game over), constructs an appropriately sized `Window`, loads the `global_sprites.pyxres` pack, and starts the Pyxel loop. It also exposes helpers (`change_to_game()`, `change_to_game_over()`, `change_to_difficulty_selector()`) that relaunch the Python process with new arguments whenever the user switches modes, ensuring each screen starts with a clean state.

### Window
`Window` centralizes the window geometry. When created with a `Difficulty` it pulls the canonical width and height from the difficulty configuration; otherwise it simply wraps the explicit width/height pair passed by callers. This keeps Pyxel initialization consistent no matter which screen is running.

### DifficultySelectorScreen
`DifficultySelectorScreen` is the landing menu. It renders the controls legend, listens for number keys to pick a difficulty, plays a confirmation sound, and hands control back to `App.change_to_game()` once the chime finishes so the game launches on the chosen difficulty.

### GameOverScreen
`GameOverScreen` appears when the player loses all lives. It shows the defeat message alongside the final score and survival time, and waits for either `ESC` to quit Pyxel or `SPACE` to relaunch via `App.change_to_difficulty_selector()` so the player can try again.

### GameApp
`GameApp` is the in-game screen. It receives the fully built `Game`, the HUD `PyxelElement`s, and the controller bindings, then drives the simulation loop: throttling package/truck movement ticks, checking for key presses, synchronizing package sprites with their states, refreshing HUD counters, and orchestrating boss visits through the `Door`/`Boss` pair. When the truck fills up or the players lose all lives, it signals the `App` to swap screens.

### Controller
Command class that facilitates handling user input by providing a unified interface for each function.

```python
class Controller:
  def execute(self):
    ...
```

### MoveUpPlayer
`MoveUpPlayer` is a `Controller` bound to the keys that move a specific `Player` one floor higher by calling `Game.move_player_up()`.

### MoveDownPlayer
`MoveDownPlayer` mirrors the controller above and triggers `Game.move_player_down()` to descend a floor.

### PyxelElement

Class that renders an object in the application based on game elements and frames data.

`PyxelStaticElement` is used for the same purpose, but it does not need an object to display. Accordingly, it is __static__. It is used for stage decorations.

`Frame` stores information about images. It is used to display several photos for one element at once (since an element can be complex and consist of more than one image (for example, a conveyor belt)).

### Grid
`Grid` is a simple enum (`ROW` or `COLUMN`) that tells `PyxelElement` whether to lay out its frames horizontally or vertically when drawing multi-frame sprites.

### BoardedPyxelElement

Decorator for any `PyxelElement` that draws a rectangular border sized after the element's `length` and `height` (plus optional padding) before delegating to the wrapped element's `draw()`. It is intended as a _development_ aid when you need to highlight, align, or debug sprites during Pyxel scene tuning.

### PyxelApp

`PyxelApp` wires the Pyxel event loop to the game simulation: it loads sprite resources, keeps a list of `PyxelElement` instances to draw, binds `Controller`s to keyboard buttons, and advances `Game` ticks according to configurable delays for package movement and creation. On every update it polls the buttons, extends the render list with freshly spawned packages, and calls `Game.move_packages()` / `Game.create_package()` when the elapsed time exceeds the configured cadence before redrawing the scene.

## HUD helpers

### PointsCounter
`PointsCounter` tracks the thousands/hundreds/tens/ones digits shown on the scoreboard. `update_points()` validates that the score fits within four digits, splits the incoming integer into individual digits, and stores them for the renderer.

### LivesCounter
`LivesCounter` is an `Element` placeholder that marks where the lives indicator is drawn. All logic for adding or removing lives happens in `Game`, but the element lets Pyxel position the corresponding sprites.

### DeliveriesCounter
`DeliveriesCounter` mirrors `LivesCounter` for the delivered-package counter. It anchors the HUD location where the total deliveries (and thus bonus-life thresholds) are displayed.

### CanRecievePackage
`CanRecievePackage` is a typing protocol for any object that accepts `Package` instances via `put_package()`. Conveyors, floors, and the truck conform to it so type checkers can validate package transfers.

## Entry point

### `main()`
`main()` lives in `game/main.py` and acts as the CLI bridge into Pyxel. It parses up to five optional integers passed on the command line (window width/height, difficulty preset, carried-over points, seconds survived) and forwards them to `App`. When arguments are omitted they remain `None`, allowing the app to fall back to the defaults baked into the presentation layer.

# Main Algorithms
- `Game.move_packages()` is the heart of the loop. First, it inspects every `Conveyor` for a `falling_package`. If the target `finish_floor` hosts a `Player`, the player briefly picks that package, drops it toward the `next_conveyor`, and the controller inserts it onto the next belt; otherwise a dropped package decrements `live_amount`. After resolving transfers it calls `Conveyor.move_packages()` on each belt and increments the global `tick`.
- `Conveyor.move_packages()` iterates through its `_packages`, offsets each package horizontally by `velocity` toward `direction`, and checks `_is_package_on_conveyor()`. Packages that have moved beyond the physical span are marked `FALLING`, recorded as `falling_package`, and removed via `lift_package()` so they can be caught by the next floor.
- `Game.move_player_up()` / `move_player_down()` take a `Player`, find their current `Floor` within the allowed tuple, and move exactly one step toward the target tier. They guard against moving past the ends of the tuple and raise a `DomainError` if a player's coordinates no longer match any known floor.
- `Game.create_package()` asks every `PackageFactory` to `create_package()`, which in turn spawns a `Package` at the configured coordinates and places it on a belt so it joins the next simulation step automatically.
- `Truck.put_package()` is the terminal sink: whenever an external actor loads a package on the truck, it flips the package state to `ON_TRUCK` and enforces the eight-package capacity via `is_full()`.


# Performed work

Throughout the project, we tried to make it as easy to understand and scalable as possible. We divided the project into two layers. The domain, which is responsible for the business logic (game rules), and the presentation, which uses the `pyxel` library to display the game and interact with the user. All game initialisation settings are located in main.py.

All objects in the game are subclasses of the `Element` class. The game has players controlled by the user (in this case, _Mario_ and _Luigi_). Players are intermediaries between conveyors. Each conveyor knows about the next conveyor to which it will pass the package. The factory is responsible for creating packages. If the player is not in the required position when the end of the conveyor is reached, the package begins to fall. When it hits the floor, the user loses a life (the number of lives is displayed on the counter at the top right).

A difficulty level has also been implemented, which determines the number of conveyors, the size of the window, and the speed of the conveyors.

# User manual

All user actions are controlled via `Controllers`. Each `Controller` is responsible for a specific trigger (for example, moving a specific player in a specific direction (up/down)). The __W__ and __S__ buttons are used to control _Luigi_, and the ____ and ____ buttons are used to control _Mario_.

# Conclusions

It was an interesting project with an interesting task. All the necessary functionality was implemented. Emphasis was placed on code readability and scalability. The main problem was the difficulty of separating logic from presentation.

The code itself is formatted and correct due to checks using `ruff` and `mypy`. The code contains type annotations that make it easier to understand.

## Personal comments

While working on the project, we were inspired by works such as _"Design Patterns: Elements of Reusable Object-Oriented Software"_ and _"Clean Architecture"_. They helped us implement certain parts of the project and gave us a general vision of how to divide responsibilities in the code.

Teamwork was implemented through `git` and __Github__, which facilitated development by working through different branches and pull requests.

Despite all the work that has been done, there are some aspects that could be improved. Currently, Window and Difficulty bring in the global state (the game depends on the global value specified in `domain/difficulty.py` and `presentation/gui.py`).
