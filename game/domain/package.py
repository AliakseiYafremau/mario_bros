from game.domain.elements import MotionElement


class Package(MotionElement):
    def __init__(self, x, y, length, height):
        self.is_on_conveyor = False #FIXME IS IT CORRECT???
        super().__init__(x, y, length, height)