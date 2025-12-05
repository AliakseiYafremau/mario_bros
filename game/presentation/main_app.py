import pyxel
from pathlib import Path

from game.presentation.gui import Window


class App:
    def __init__(self, screens: list, initial_screen, window: Window):
        resource_path = (
                Path(__file__).resolve().parents[2] / "assets" / "global_sprites.pyxres"
        )
        self.screens: list = screens
        self.current_screen = initial_screen
        self.running_window = window

        pyxel.init(
            self.running_window.width,
            self.running_window.height,
            title="Pyxel APP",
            fps=60,
            quit_key=pyxel.KEY_ESCAPE,
        )
        pyxel.load(str(resource_path))
        pyxel.run(self.current_screen.update, self.current_screen.draw)