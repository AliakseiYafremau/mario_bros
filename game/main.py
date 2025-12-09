"""Command line entry point for the Mario Bros Pyxel application."""

import sys

from game.presentation.main_app import App


def main(
    new_width: int | None,
    new_height: int | None,
    new_difficulty_value: int | None,
    points: int | None,
    seconds_alive: int | None,
) -> None:
    """Bootstrap the Pyxel application with values passed from the CLI.

    Each argument may be None when the caller wants to rely on default values.

    :param new_width: int | None, window width in pixels or None.
    :param new_height: int | None, window height in pixels or None.
    :param new_difficulty_value: int | None, difficulty level, -1 for game over,
        or None to start at the difficulty selector.
    :param points: int | None, final score used when resuming at game over.
    :param seconds_alive: int | None, time survived used when resuming at game over.
    """
    App(
        new_width=new_width,
        new_height=new_height,
        new_difficulty_value=new_difficulty_value,
        points=points,
        seconds_alive=seconds_alive,
    )


if __name__ == "__main__":
    # Treat every CLI argument as optional so the launcher can override only the fields it needs.
    new_width = int(sys.argv[1]) if len(sys.argv) > 1 else None
    new_height = int(sys.argv[2]) if len(sys.argv) > 2 else None
    new_difficulty_value = int(sys.argv[3]) if len(sys.argv) > 3 else None
    points = int(sys.argv[4]) if len(sys.argv) > 4 else None
    seconds_alive = int(sys.argv[5]) if len(sys.argv) > 5 else None

    main(new_width, new_height, new_difficulty_value, points, seconds_alive)
