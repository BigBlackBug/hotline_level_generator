from __future__ import annotations

from dataclasses import dataclass

from .geomerty import Rect, Line, find_common_rect


# LevelConfig = namedtuple(
#     'LevelConfig', field_names=[
#         'room_number', 'max_width', 'max_height'
#     ])

@dataclass
class LevelConfig:
    room_number: int
    max_width: int
    max_height: int


class Room:
    def __init__(self, bounds: Rect):
        # bounds remain the same
        self.bounds = bounds
        self.walls = [
            Wall(self, bounds.top),
            Wall(self, bounds.right),
            Wall(self, bounds.bottom),
            Wall(self, bounds.left)
        ]

    def underlap_room(self, new_room: Room):
        """
        Rebuilds walls of this room and the new_room as if
        new_room was placed under new_room
        :param new_room: room to be placed under
        """
        common_rect = find_common_rect(self.bounds, new_room.bounds)
        used_sides = set()
        for rect_side in common_rect.sides:
            # upper section
            upper_room_walls = list(self.walls)
            for wall in upper_room_walls:
                # if rect side is part of the upper room wall
                # break this wall into pieces and make them new walls
                split = wall.line.split_via(rect_side)
                if len(split) > 1:
                    # build new walls for the target_room
                    self.walls.remove(wall)
                    self.walls.extend((
                        Wall(self, wall_piece) for wall_piece in split
                    ))

            lower_room_walls = list(new_room.walls)
            for wall in lower_room_walls:
                # if the rect side is part of the bottom room wall
                # break that wall into pieces and make them walls
                # except the ones that have same dimensions with rect_side
                split = wall.line.split_via(rect_side)
                if len(split) > 1:
                    # build new walls for the target_room
                    new_room.walls.extend((
                        Wall(new_room, wall_piece) for wall_piece in split
                        if wall_piece != rect_side
                    ))
                if len(split) >= 1:
                    new_room.walls.remove(wall)
                    used_sides.add(rect_side)

        for rect_side in common_rect.sides:
            if rect_side not in used_sides:
                new_room.walls.append(Wall(new_room, rect_side))

    def connect(self, target_room: Room):
        """
        Goes through all of the walls of both rooms
        and connects them to each other
        :param target_room:
        """
        for my_wall in self.walls:
            for other_wall in target_room.walls:
                if my_wall.line == other_wall.line:
                    my_wall.connect(other_wall)
                    other_wall.connect(my_wall)

    def __str__(self):
        return f"Room id={id(self)}, \n" \
               f"{', '.join(map(str, self.walls))}"


class Wall:
    def __init__(self, room: Room, line: Line,
                 thickness: int = 0):
        self._line = Line(line.start, line.end)
        # TODO thickness is not taken into account anywhere
        self._thickness = thickness
        self.shared_wall = None
        self.room = room

    def __eq__(self, other):
        return self._line == other.line and \
               id(self.room) == id(other.room)

    def __hash__(self):
        return super().__hash__()

    @property
    def line(self) -> Line:
        return self._line

    def connect(self, wall):
        self.shared_wall = wall

    def __str__(self):
        return f"Wall {self._line}"
