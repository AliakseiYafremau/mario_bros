from game.domain.elements import Element
from game.presentation.app import PyxelApp
from game.presentation.pyxel_elements import PyxelElement


def main():
    square = Element(100, 100, 100, 100)
    rendered_square = PyxelElement(square, 0, 0, 0, 15, 15)
    PyxelApp(rendered_square)


if __name__ == "__main__":
    main()
