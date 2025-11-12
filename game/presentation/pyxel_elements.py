import pyxel

from game.domain.elements import Element


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
    ):
        self.element = element
        self.frames = frames

    def draw(self):
        for frame in self.frames:
            pyxel.blt(
                x=self.element.x,
                y=self.element.y,
                img=frame.image,
                u=frame.u,
                v=frame.v,
                w=frame.w,
                h=frame.h,
                colkey=frame.colkey,
                rotate=frame.rotate,
                scale=frame.scale,
            )
