import sys
import subprocess
from pathlib import Path

import pyxel

from game.game_setup import create_game_app
from game.domain.difficulty import Difficulty
from game.presentation.window import Window
from game.presentation.difficulty_selector import DifficultySelectorScreen
from game.presentation.game_over import GameOverScreen


class App:
    """Bootstrap class responsible for selecting the right screen and relaunching.

    This class initializes Pyxel, chooses the initial screen (gameplay,
    game over or difficulty selector) and offers helpers to restart the
    process with different parameters.
    """

    def __init__(
        self,
        new_width: int | None,
        new_height: int | None,
        new_difficulty_value: int | None,
        points: int | None,
        seconds_alive: float | None,
    ) -> None:
        """Initializes the application and starts the Pyxel loop.

        :param new_width: int | None, width for the window or None for defaults.
        :param new_height: int | None, height for the window or None for defaults.
        :param new_difficulty_value: int | None, difficulty level or -1 for game over.
        :param points: int | None, final score when resuming on game over.
        :param seconds_alive: float | None, time survived when resuming on game over.
        """
        resource_path = (
            Path(__file__).resolve().parents[2] / "assets" / "global_sprites.pyxres"
        )

        # Determine which screen to boot into (gameplay, game over, or selector).
        if new_difficulty_value is not None and new_difficulty_value != -1:
            self.current_screen = create_game_app(
                selected_difficulty=Difficulty(new_difficulty_value),
                app=self,
            )
        elif new_difficulty_value is not None and new_difficulty_value == -1:
            self.current_screen = GameOverScreen(
                app=self,
                points=points if points is not None else 0,
                seconds_alive=seconds_alive if seconds_alive is not None else 0.0,
            )
        else:
            self.current_screen = DifficultySelectorScreen(app=self)

        # If window size is passed via args reuse it, otherwise fall back to menu defaults.
        if new_width is not None and new_height is not None:
            running_window = Window(width=new_width, height=new_height)
        else:
            running_window = Window(width=200, height=175)

        pyxel.init(
            running_window.width,
            running_window.height,
            title="Mario Bros. --- Game & Watch",
            fps=60,
            quit_key=pyxel.KEY_ESCAPE,
        )
        pyxel.fullscreen(True)
        pyxel.load(str(resource_path))
        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        """Delegates update logic to the current screen."""
        self.current_screen.update()

    def draw(self) -> None:
        """Delegates draw logic to the current screen."""
        self.current_screen.draw()

    @staticmethod
    def change_to_game(difficulty_value: int) -> None:
        """Restart the process and start the game screen.

        :param difficulty_value: int, selected difficulty level.
        """
        new_running_window = Window(difficulty=Difficulty(difficulty_value))
        project_root = Path(__file__).resolve().parents[2]

        subprocess.Popen(
            [
                sys.executable,
                "-m",
                "game.main",
                str(new_running_window.width),
                str(new_running_window.height),
                str(difficulty_value),
            ],
            cwd=project_root,
        )

        sys.exit(0)

    @staticmethod
    def change_to_game_over(points: int, seconds_alive: float) -> None:
        """Restart the process and start the game-over screen.

        :param points: int, final score.
        :param seconds_alive: float, time survived.
        """
        new_running_window = Window(width=200, height=175)
        project_root = Path(__file__).resolve().parents[2]

        subprocess.Popen(
            [
                sys.executable,
                "-m",
                "game.main",
                str(new_running_window.width),
                str(new_running_window.height),
                str(-1),
                str(points),
                str(seconds_alive),
            ],
            cwd=project_root,
        )

        sys.exit(0)

    @staticmethod
    def change_to_difficulty_selector() -> None:
        """Restart the process and return to the difficulty selection screen."""
        new_running_window = Window(width=200, height=175)
        project_root = Path(__file__).resolve().parents[2]

        subprocess.Popen(
            [
                sys.executable,
                "-m",
                "game.main",
                str(new_running_window.width),
                str(new_running_window.height),
            ],
            cwd=project_root,
        )

        sys.exit(0)
