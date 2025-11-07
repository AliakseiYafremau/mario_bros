from game.domain.player import Player


class Floor:
    def __init__(self, x, y, player: Player):
        self.x = x
        self.y = y
        self.player = player
