import pyxel

from game.domain.elements import Element


class PyxelElement(Element):
    def __init__(
        self,
        element: Element,
        image: int,
        u: int,
        v: int,
        w: int,
        h: int,
        colkey: int | None = None,
        rotate: int | None = None,
        scale: int | None = None,
    ):
        self.element = element
        self.image = image
        self.u = u
        self.v = v
        self.w = w
        self.h = h
        self.colkey = colkey
        self.rotate = rotate
        self.scale = scale

    def draw(self):
        pyxel.blt(
            x=self.element.x,
            y=self.element.y,
            img=self.image,
            u=self.u,
            v=self.v,
            w=self.w,
            h=self.h,
            colkey=self.colkey,
            rotate=self.rotate,
            scale=self.scale,
        )
