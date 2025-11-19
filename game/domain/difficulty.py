import random

class Difficulties():
    EASY = 0
    MEDIUM = 1
    EXTREME = 2
    CRAZY = 3

class Difficulty:
    def __init__(self, difficulty: Difficulties = 0):
        self.difficulty = difficulty

    @property
    def difficulty(self):
        return self.__difficulty

    @difficulty.setter
    def difficulty(self, value):
        if isinstance(value, Difficulties):
            self.__difficulty = value
        else:
            raise TypeError("The difficulty must be of class Difficulties")

class DifficultyValues:
    def __init__(self):
        BELTS = (5, 7, 9, 5)
        CONVEYOR_SPEED = ((1, 1, 1), (1, 1, 1.5), (1, 1.5, 2), (1, random.uniform(1, 2), random.uniform(1, 2)))
        INCREASE = (50, 30, 30, 20)
        ELIMINATES = (3, 5, 5, 0)
        if Difficulty.difficulty == 3:
            self.reversed_controls = True
        else:
            self.reversed_controls = False

        self.belts = BELTS[Difficulty.difficulty]
        self.conveyor_speed = CONVEYOR_SPEED[Difficulty.difficulty]
        self.increase = INCREASE[Difficulty.difficulty]
        self.eliminates = ELIMINATES[Difficulty.difficulty]
