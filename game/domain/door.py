from game.domain.elements import Element
from game.domain.boss import Boss


class Door(Element):
    """Doorway that controls when the `Boss` sprite enters the scene."""

    def __init__(self,
                 x: int,
                 y: int,
                 length: int,
                 height: int,
                 boss: Boss):
        self.boss: Boss = boss
        super().__init__(x, y, length, height)
