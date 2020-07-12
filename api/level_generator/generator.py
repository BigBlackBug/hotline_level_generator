import random
from collections import defaultdict
from dataclasses import dataclass

from api.level_generator import geometry
from api.level_generator.geometry import CornerEnum, Rect
from api.level_generator.models import Room, Map

_MAX_ATTEMPTS = 10
MIN_SQUARE_K = 0.003
MAX_SQUARE_K = 0.05


class Holder:
    def __init__(self, widths, heights, ):
        self.widths = widths
        self.heights = heights


@dataclass
class CornerKey:
    x: int
    y: int
    corner: CornerEnum

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y \
               and self.corner == other.corner

    def __hash__(self):
        return hash((self.x, self.y, self.corner))


class Generator:
    def __init__(self, map_width, map_height):
        self.map = Map((map_width, map_height))
        self.corner_cache = defaultdict(Holder)

    # place_room_above
    # see if the room is split into disjoint rooms
    # validate disjoint rooms and make unique
    def generate(self, room_number):
        """
        Generates a level graph
        :param level_config:
        :return: list of Rooms
        """
        first_room = self._make_first_room()
        print(f" first room bounds{first_room.bounds}")
        rooms = [first_room]
        for _ in range(room_number - 1):
            room = self._add_new_room(rooms)
            rooms.append(room)
        # TODO check disjoint rooms
        # TODO get rid of
        return rooms

    def _make_first_room(self):
        x, y = int(self.map.width / 2), \
               int(self.map.height / 2)
        width = random.randint(int(self.map.width / 8) + 1,
                               int(self.map.width / 3) + 1)
        height = random.randint(int(self.map.height / 8) + 1,
                                int(self.map.height / 3) + 1)
        rect = Rect.make_rect((x, y), width, height)
        return self._place_room_above(rect)

    def _place_room_above(self, rect):
        new_room = Room(rect)
        x, y, width, height = rect.origin[0], rect.origin[1], \
                              rect.width, rect.height
        for tile in self.map.next_tiles(x, y, width, height):
            if tile.lies_on_rect_bounds((x, y), width, height):
                bottom_room = tile.room
                tile.clear()

                is_corner = tile.is_corner((x, y), width, height)
                new_room.add_wall(tile, bottom_room, is_corner)
            else:
                tile.clear()
                new_room.add_tile(tile)

        return new_room

    def _add_new_room(self, rooms: list):
        above_room = None
        while not above_room:
            target_room = self._pick_room(rooms)
            above_room = self._make_new_room(target_room)

        return above_room

    def _pick_room(self, rooms):
        # TODO a more intelligent algorithm
        return random.choice(rooms)

    def _make_new_room(self, target_room):
        # TODO pick a tile
        attempts = 0
        while attempts != _MAX_ATTEMPTS:
            try:
                start_tile = random.choice(list(target_room.tiles))
                print(f"picked start_tile {start_tile.x},{start_tile.y}")
                if not start_tile.has_neighboring_walls(self.map):
                    widths_left, widths_right = \
                        self.map.calculate_room_widths(start_tile, target_room)
                    heights_top, heights_bottom = \
                        self.map.calculate_room_heights(start_tile, target_room)
                    corner = geometry.CornerEnum.random()

                    min_square = MIN_SQUARE_K * self.map.square
                    max_square = MAX_SQUARE_K * self.map.square
                    width, height = self.pick_dimensions(
                        corner, widths_left, widths_right,
                        heights_top, heights_bottom,
                        min_square=min_square, max_square=max_square)
                    print(f"got corner {corner}, w={width}, h={height}")
                    origin = geometry.transform_origin(
                        (start_tile.x, start_tile.y),
                        width, height, corner)
                    print(f"transforming origin to {origin}")
                    rect = Rect.make_rect(origin, width, height)
                    print(f"new room rect {rect}")
                    return self._place_room_above(rect)
            except Exception as e:
                print(str(e))
            finally:
                attempts += 1

        print('failed to place a room')
        return None

    def pick_dimensions(self, corner, left, right, top, bottom, max_ratio=4,
                        min_square=50, max_square=1000):
        attempts = 0
        while attempts < _MAX_ATTEMPTS:
            if corner == CornerEnum.LT:
                width, height = random.choice(right), random.choice(bottom)
            elif corner == CornerEnum.LB:
                width, height = random.choice(right), random.choice(top)
            elif corner == CornerEnum.RT:
                width, height = random.choice(left), random.choice(bottom)
            else:
                # RB
                width, height = random.choice(left), random.choice(top)
            if max(width / height, height / width) < max_ratio and \
                    min_square < width * height < max_square:
                return width, height
            attempts += 1
        raise KeyError("Unable to pick valid dimensions. Try a new tile")
