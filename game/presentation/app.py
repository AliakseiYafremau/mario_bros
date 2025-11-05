import pyxel

from game.domain.elements import Element
from game.domain.game import Game


class PyxelElement(Element):
    def __init__(self, x, y, length, height, image_path: str):
        self.image_path = image_path
        super().__init__(x, y, length, height)


class PyxelApp:
    def __init__(self, game: Game):
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pass
