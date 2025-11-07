from game.domain.player import Player


class Floor:
    def __init__(self, x, y, player: Player | None = None):
        self.x = x
        self.y = y
        self.player = player

    def __eq__(self, value):
        return self.x == value.x and self.y == value.y
