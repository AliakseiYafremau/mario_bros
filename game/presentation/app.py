from pathlib import Path

import pyxel
from game.presentation.scenes.base import SceneManager


class PyxelApp:
    def __init__(self, manager: SceneManager) -> None:
        self.manager = manager

        resource_path = (
            Path(__file__).resolve().parents[2] / "assets" / "global_sprites.pyxres"
        )

        pyxel.init(418, 173, title="Pyxel APP")
        pyxel.load(str(resource_path))
        pyxel.run(self.get_update, self.get_draw)

    def get_update(self):
        return self.manager.get_current_scene().update()

    def get_draw(self):
        return self.manager.get_current_scene().draw()
