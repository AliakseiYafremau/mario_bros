import pyxel

from game.domain.game import Game


class PyxelApp:
    def __init__(self, game: Game):
        pyxel.run(self.update, self.draw)
    
    def update(self):
        pass

    def draw(self):
        pass