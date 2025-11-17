from enum import Enum
import pyxel

from game.domain.elements import Element
from game.domain.logging import get_logger


logger = get_logger(__name__, "PRESENTATION")


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
        logger.debug(
            "%s was created in (x=%s, y=%s)",
            self.element,
            self.element.x,
            self.element.y,
        )

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
                element_x += frame.h
            elif self.grid == Grid.COLUMN:
                element_y += frame.w
            else:
                raise ValueError("Invalid Grid type")


class PyxelStaticElement(PyxelElement):
    def __init__(self, x: int, y: int, *frames: Frame, grid: Grid = Grid.ROW):
        self.x = x
        self.y = y
        self.frames = frames
        self.grid = grid

    def draw(self):
        element_x = self.x
        element_y = self.y

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
                element_x += frame.h
            elif self.grid == Grid.COLUMN:
                element_y += frame.w
            else:
                raise ValueError("Invalid Grid type")
