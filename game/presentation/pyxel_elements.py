from enum import Enum
import pyxel

from game.domain.elements import Element


class Grid(Enum):
    ROW = "row"
    COLUMN = "column"


class Frame:
    def __init__(
        self,
        image: int,
        u: int,
        v: int,
        w: int,
        h: int,
        colkey: int | None = None,
        rotate: int | None = None,
        scale: int | None = None,
    ):
        self.image = image
        self.u = u
        self.v = v
        self.w = w
        self.h = h
        self.colkey = colkey
        self.rotate = rotate
        self.scale = scale


class PyxelElement(Element):
    def __init__(
        self,
        element: Element,
        *frames: Frame,
        grid: Grid = Grid.ROW,
    ):
        self.element = element
        self.frames = frames
        self.grid = grid

    def draw(self):
        element_x = self.element.x
        element_y = self.element.y

        for frame in self.frames:
            pyxel.blt(
                x=element_x,
                y=element_y,
                img=frame.image,
                u=frame.u,
                v=frame.v,
                w=frame.w,
                h=frame.h,
                colkey=frame.colkey,
                rotate=frame.rotate,
                scale=frame.scale,
            )

            if self.grid == Grid.ROW:
                element_x += frame.h * (frame.scale if frame.scale else 1)
            elif self.grid == Grid.COLUMN:
                element_y += frame.w * (frame.scale if frame.scale else 1)
            else:
                raise ValueError("Invalid Grid type")


class PyxelStaticElement(PyxelElement):
    def __init__(self, x: int, y: int, *frames: Frame, grid: Grid = Grid.ROW):
        self.element = Element(x, y, 0, 0)
        self.frames = frames
        self.grid = grid

    def draw(self):
        element_x = self.element.x
        element_y = self.element.y

        for frame in self.frames:
            pyxel.blt(
                x=element_x,
                y=element_y,
                img=frame.image,
                u=frame.u,
                v=frame.v,
                w=frame.w,
                h=frame.h,
                colkey=frame.colkey,
                rotate=frame.rotate,
                scale=frame.scale,
            )

            if self.grid == Grid.ROW:
                element_x += frame.h * (frame.scale if frame.scale else 1)
            elif self.grid == Grid.COLUMN:
                element_y += frame.w * (frame.scale if frame.scale else 1)
            else:
                raise ValueError("Invalid Grid type")


class BoardedPyxelElement(PyxelElement):
    def __init__(
        self,
        element: PyxelElement,
        padding: int = 1,
        color: int = 7,
    ):
        self.decorated = element
        self.padding = padding
        self.color = color

    @property
    def element(self):
        return self.decorated.element

    def draw(self):
        target = self.decorated.element

        border_x = target.x - self.padding
        border_y = target.y - self.padding
        border_width = target.length + self.padding * 2
        border_height = target.height + self.padding * 2

        pyxel.rectb(
            x=border_x,
            y=border_y,
            w=border_width,
            h=border_height,
            col=self.color,
        )
        self.decorated.draw()
