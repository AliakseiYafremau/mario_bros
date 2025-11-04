from game.domain.directions import Direction
from game.domain.elements import Element


class Conveyor(Element):
    def __init__(self, x: int, y: int, weigth: int, height: int, direction: Direction, velocity: int):
        self.direction = direction
        self.velocity = velocity
        self._packages = []
        super().__init__(x, y, weigth, height)
    
    @property
    def velocity(self):
        return self._velocity
    
    @property
    def direction(self):
        return self._direction
    
    @velocity.setter
    def velocity(self, value):
        if value < 0:
            raise ValueError("Velocity cannot be negative")
        self._velocity = value

    @direction.setter
    def direction(self, value):
        if not isinstance(value, Direction):
            raise TypeError("direction must be a Direction instance")
        self._direction = value