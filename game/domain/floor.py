from game.domain.player import Player


class Floor:
    def __init__(self, x: int, y: int, player: Player | None = None) -> None:
        self.x = x
        self.y = y
        self.player = player

    def __eq__(self, value) -> bool:
        return self.x == value.x and self.y == value.y
