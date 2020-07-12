from __future__ import annotations

import enum
import random
from typing import List


class Line:
    def __init__(self, start: tuple, end: tuple):
        if end[0] < start[0] or end[1] < start[1]:
            raise ValueError("Invalid Line")
        self.start = start
        self.end = end

    def horizontally_overlaps(self, other: Line):
        return self.is_horizontal and other.is_horizontal and \
               self.y == other.y and self._overlaps(other, 'x')

    def vertically_overlaps(self, other: Line):
        return self.is_vertical and other.is_vertical and \
               self.x == other.x and self._overlaps(other, 'y')

    def _overlaps(self, other: Line, coord: str):
        i = 0 if coord == 'x' else 1
        return min(self.end[i], other.end[i]) >= max(
            self.start[i], other.start[i])

    def split_via(self, other: Line):
        """
        Calculates an intersection between this line and the other and
        returns a list of Lines that make up this line

        empty list - no intersection
        len(list) == 1 - lines are the same, return [this line]
        len(list) > 1 -  [line pieces]
        :param other:
        :return: list of Lines that make up the original Line
        """
        # both horizontal
        result = []
        if self.horizontally_overlaps(other):
            points = sorted({self.start[0], self.end[0],
                             other.start[0], other.end[0]})
            for i in range(len(points) - 1):
                result.append(Line((points[i], self.y),
                                   (points[i + 1], self.y)))
        elif self.vertically_overlaps(other):
            points = sorted({self.start[1], self.end[1],
                             other.start[1], other.end[1]})
            for i in range(len(points) - 1):
                result.append(Line((self.x, points[i]),
                                   (self.x, points[i + 1])))
        return result

    @property
    def is_horizontal(self):
        return self.y is not None

    @property
    def is_vertical(self):
        return self.x is not None

    @property
    def x(self):
        return self.start[0] if self.start[0] == self.end[0] else None

    @property
    def y(self):
        return self.start[1] if self.start[1] == self.end[1] else None

    def __repr__(self):
        return f"({self.start}, {self.end})"

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __hash__(self):
        return super().__hash__()

    def __str__(self):
        return f"[{self.start}, {self.end}]"


class Rect:
    def __init__(self, top: Line, right: Line, bottom: Line, left: Line):
        self.top, self.right, self.bottom, self.left = \
            top, right, bottom, left

    @classmethod
    def make_rect(cls, origin: tuple, width: int, height: int) -> Rect:
        # TODO validate max_bounds
        if origin[0] < 0 or origin[1] < 0:
            raise ValueError(f"origin point {origin} beyond [0,0]")
        return Rect(Line(origin, (origin[0] + width, origin[1])),
                    Line((origin[0] + width, origin[1]),
                         (origin[0] + width, origin[1] + height)),
                    Line((origin[0], origin[1] + height),
                         (origin[0] + width, origin[1] + height)),
                    Line(origin, (origin[0], origin[1] + height)))

    @property
    def sides(self) -> List[Line]:
        """
        :return: List of Lines in clockwise order
        """
        return [self.top, self.right, self.bottom, self.left]

    @property
    def width(self):
        return self.top.end[0] - self.top.start[0]

    @property
    def height(self):
        return self.left.end[1] - self.top.start[1]

    @property
    def origin(self):
        return self.left.start[0], self.top.start[1]

    def __eq__(self, other):
        return self.top == other.top and self.right == other.right and \
               self.bottom == other.bottom and self.left == other.left

    def __hash__(self):
        return super().__hash__()

    def __repr__(self):
        return f"{self.top}, {self.right}, {self.bottom}, {self.left}"


def find_common_rect(rect_1: Rect, rect_2: Rect):
    """
    Returns a Rect instance out of common space between rect_1 and rect_2
    or None if Rects do not overlap
    :param rect_1:
    :param rect_2:
    :return:
    """
    left_x = max(rect_1.left.x, rect_2.left.x)
    right_x = min(rect_1.right.x, rect_2.right.x)
    top_y = max(rect_1.top.y, rect_2.top.y)
    bottom_y = min(rect_1.bottom.y, rect_2.bottom.y)

    if left_x < right_x and top_y < bottom_y:
        return Rect.make_rect(origin=(left_x, top_y),
                              width=right_x - left_x,
                              height=bottom_y - top_y)
    return None


def make_point_inside(bounds: Rect):
    x = random.randint(bounds.left.x + 1, bounds.right.x - 1)
    y = random.randint(bounds.top.y + 1, bounds.bottom.y - 1)
    return x, y


class CornerEnum(enum.Enum):
    LT = enum.auto(),
    RT = enum.auto(),
    RB = enum.auto(),
    LB = enum.auto()

    @staticmethod
    def random():
        return random.choice(list(CornerEnum))


def transform_origin(origin, width, height, corner=CornerEnum.LT):
    if corner == CornerEnum.RT:
        return origin[0] - width, origin[1]
    elif corner == CornerEnum.RB:
        return origin[0] - width, origin[1] - height
    elif corner == CornerEnum.LB:
        return origin[0], origin[1] - height
    return origin
