from game.presentation.pyxel_elements import (
    BoardedPyxelElement,
    Frame,
    Grid,
    PyxelElement,
)

class Window:
    __instance = None

    def __new__(cls, width=800, height=600):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.width = width
            cls.__instance.height = height
        return cls.__instance
