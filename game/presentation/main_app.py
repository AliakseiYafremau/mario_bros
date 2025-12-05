import pyxel
from pathlib import Path

from game.domain.difficulty import Difficulty
from game.game_setup import create_game_app
from game.presentation.gui import Window
from game.presentation.difficulty_selector import DifficultySelectorScreen


class App:
    def __init__(self):
        resource_path = (
                Path(__file__).resolve().parents[2] / "assets" / "global_sprites.pyxres"
        )
        self.current_screen = DifficultySelectorScreen(app=self)
        self.running_window = Window(Difficulty(0))

        pyxel.init(
            self.running_window.width,
            self.running_window.height,
            title="Pyxel APP",
            fps=60,
            quit_key=pyxel.KEY_ESCAPE,
        )
        pyxel.load(str(resource_path))
        pyxel.run(self.update, self.draw)

    def update(self):
        self.current_screen.update()

    def draw(self):
        self.current_screen.draw()

    def change_to_game(self, difficulty: Difficulty) -> None:
        game_app = create_game_app(difficulty)
        self.current_screen = game_app
