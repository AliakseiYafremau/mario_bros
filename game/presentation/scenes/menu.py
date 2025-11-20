import pyxel
from game.presentation.controllers import Controller
from game.presentation.scenes.base import Scene


class Menu(Scene):
    def __init__(self, buttons: dict[int, Controller]):
        self.buttons = buttons

    def update(self) -> None:
        for button in self.buttons:
            if pyxel.btnp(button):
                self.buttons[button].execute()

    def draw(self) -> None:
        pyxel.cls(0)
        pyxel.text(150, 80, "Press 1 to Start Game", pyxel.frame_count % 16)