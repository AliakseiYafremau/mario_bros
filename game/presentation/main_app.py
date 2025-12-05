import pyxel
import sys
import subprocess
from pathlib import Path

from game.domain.difficulty import Difficulty
from game.game_setup import create_game_app
from game.presentation.gui import Window
from game.presentation.difficulty_selector import DifficultySelectorScreen


class App:
    def __init__(self, new_width: int | None,
                 new_height: int | None,
                 new_difficulty_value: int | None):
        resource_path = (
                Path(__file__).resolve().parents[2] / "assets" / "global_sprites.pyxres"
        )

        if new_difficulty_value is not None:
            self.current_screen = create_game_app(selected_difficulty=Difficulty(new_difficulty_value))
        else:
            self.current_screen = DifficultySelectorScreen(app=self)

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

    def update(self):
        self.current_screen.update()

    def draw(self):
        self.current_screen.draw()

    def change_to_game(self, difficulty_value) -> None:
        new_running_window = Window(difficulty=Difficulty(difficulty_value))

        project_root = Path(__file__).resolve().parents[2]

        subprocess.Popen([
            sys.executable,
            "-m", "game.main",
            str(new_running_window.width),
            str(new_running_window.height),
            str(difficulty_value)
        ], cwd=project_root)

        sys.exit(0)
