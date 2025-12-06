from game.domain.elements import Element


class Boss(Element):
    def __init__(self,
                 x: int,
                 y: int,
                 length: int,
                 height: int):
        self.comes_in_time: int = 0
        self.has_to_leave: bool = False
        super().__init__(x, y, length, height)
