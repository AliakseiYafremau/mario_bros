from enum import Enum

import pyxel

from game.domain.elements import Element


class Grid(Enum):
    """Frame layout variants for multi-frame Pyxel elements."""

    ROW = "row"
    COLUMN = "column"


class Frame:
    """Lightweight container that stores Pyxel blit parameters.

    Attributes:
        image (int): Index of the Pyxel image bank.
        u (int): x-coordinate of the sprite inside the bank.
        v (int): y-coordinate of the sprite inside the bank.
        w (int): width of the sprite.
        h (int): height of the sprite.
        colkey (int | None): transparency color key.
        rotate (int | None): rotation flag for Pyxel.
        scale (int | None): scaling factor.
    """

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
    ) -> None:
        """Initializes a frame with sprite parameters.

        :param image: int, image bank index.
        :param u: int, x-coordinate in the bank.
        :param v: int, y-coordinate in the bank.
        :param w: int, width of the sprite.
        :param h: int, height of the sprite.
        :param colkey: int | None, transparency color key.
        :param rotate: int | None, rotation mode.
        :param scale: int | None, scaling factor.
        """
        self.image = image
        self.u = u
        self.v = v
        self.w = w
        self.h = h
        self.colkey = colkey
        self.rotate = rotate
        self.scale = scale


class PyxelElement(Element):
    """Bridge that draws a domain :class:`Element` using sprite frames.

    Attributes:
        element (Element): Domain element with position/size.
        frames (tuple[Frame, ...]): Frames used to render the element.
        grid (Grid): Grid layout used to stack frames.
    """

    def __init__(
        self,
        element: Element,
        *frames: Frame,
        grid: Grid = Grid.ROW,
    ) -> None:
        """Initializes the PyxelElement.

        :param element: Element, the domain element to draw.
        :param frames: Frame, one or more frames to use when drawing.
        :param grid: Grid, layout to align frames (row or column).
        """
        # We reuse the domain element's coordinates and size
        super().__init__(element.x, element.y, element.length, element.height)
        self.element = element
        self.frames = frames
        self.grid = grid

    def draw(self) -> None:
        """Puts every frame using the configured grid alignment."""
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
    """`PyxelElement` variant for HUD/decoration sprites.

    This variant has no backing domain object other than a dummy
    :class:`Element` created at the given coordinates.
    """

    def __init__(self, x: int, y: int, *frames: Frame, grid: Grid = Grid.ROW) -> None:
        """Initializes a static Pyxel element.

        :param x: int, x-coordinate of the sprite.
        :param y: int, y-coordinate of the sprite.
        :param frames: Frame, one or more frames to blit.
        :param grid: Grid, layout to align frames (row or column).
        """
        element = Element(x, y, 0, 0)
        super().__init__(element, *frames, grid=grid)

    # draw behavior is inherited from PyxelElement


class BoardedPyxelElement(PyxelElement):
    """FOR DEBUG USE: renders a border around another `PyxelElement`.

    Attributes:
        decorated (PyxelElement): The element being decorated.
        padding (int): Padding between the border and the element.
        color (int): Color used for the border.
    """

    def __init__(
        self,
        element: PyxelElement,
        padding: int = 1,
        color: int = 7,
    ) -> None:
        """Initializes the decorated Pyxel element.

        :param element: PyxelElement, the element to decorate.
        :param padding: int, padding around the element.
        :param color: int, color used for the border.
        """
        self.decorated = element
        self.padding = padding
        self.color = color

    @property
    def element(self) -> Element:
        """Returns the domain element of the decorated Pyxel element.

        :return: Element, the underlying domain element.
        """
        return self.decorated.element

    def draw(self) -> None:
        """Draws a border around the decorated element and then the element itself."""
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
