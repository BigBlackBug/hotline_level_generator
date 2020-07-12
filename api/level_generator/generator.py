import random
from collections import defaultdict
from dataclasses import dataclass

from api.level_generator import geometry
from api.level_generator.geometry import CornerEnum, Rect
from api.level_generator.models import Room, Map

_MAX_ATTEMPTS = 10


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
    # recalculate corners on a new room
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
        # self.recalculate_potential_corners(first_room)
        rooms = [first_room]
        for _ in range(room_number - 1):
            room = self._add_new_room(rooms)
            rooms.append(room)
            # for room in rooms:
            #     self.recalculate_potential_corners(room)
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
        """
        Generates a new room that underlaps the target_room
        and intersects with no other room from rooms

        :param width:
        :param height:
        :param target_room:
        :param other_rooms:
        :param level_config:
        :return:
        """
        # TODO pick a tile
        attempts = 0
        while attempts != 10:
            start_tile = random.choice(list(target_room.tiles))
            print(f"picked start_tile {start_tile.x},{start_tile.y}")
            if not start_tile.has_neighboring_walls(self.map):
                try:
                    widths_left, widths_right = self.map.calculate_room_widths(
                        start_tile,
                        target_room)
                    heights_top, heights_bottom = self.map.calculate_room_heights(
                        start_tile,
                        target_room)
                    corner = geometry.CornerEnum.random()

                    width, height = self.get_wh(corner, widths_left,
                                                widths_right, heights_top,
                                                heights_bottom)
                    print(f"got corner {corner}, w={width}, h={height}")
                    origin = geometry.transform_origin(
                        (start_tile.x, start_tile.y),
                        width, height, corner)
                    print(f"transforming origin to {origin}")
                    rect = Rect.make_rect(origin, width, height)
                    print(f"new room rect {rect}")
                    attempts += 1
                except Exception as e:
                    raise e
                else:
                    return self._place_room_above(rect)
            print('failed to place a room')
            return None
        # corner = geometry.CornerEnum.random()
        # print(f"selecting corner {corner}")
        # # key = CornerKey(start_tile.x, start_tile.y, corner)
        # key,holder = random.choice(list(self.corner_cache.items()))
        # widths = holder.widths
        # heights = holder.heights
        #     # pick
        # width, height = random.choice(widths), random.choice(heights)
        # print(f"transforming {(key.x, key.y)}, w={width}, h={height}")
        # origin = geometry.transform_origin((key.x, key.y),
        #                                    width, height, corner)
        # print(f"result {origin}, w={width}, h={height}")
        # rect = Rect.make_rect(origin, width, height)
        return self._place_room_above(rect)

    def recalculate_potential_corners(self, room):
        # CornerKey -> [widths, heights]
        # result = dict()
        print(f"recalculating corners for room {room.bounds}")
        for tile in room.tiles:
            if not tile.has_neighboring_walls(self.map):
                print(f"processing tile {tile}")
                left, right = self.map.calculate_room_widths(tile, room)
                top, bottom = self.map.calculate_room_heights(tile, room)
                self.save_cache(tile, left, right, top, bottom)

    def save_cache(self, tile, left, right, top, bottom):
        self.corner_cache[CornerKey(tile.x, tile.y, CornerEnum.LT)] = \
            Holder(widths=right, heights=bottom)

        self.corner_cache[
            CornerKey(tile.x, tile.y, CornerEnum.LB)] = \
            Holder(widths=right, heights=top)

        self.corner_cache[
            CornerKey(tile.x, tile.y, CornerEnum.RT)] = \
            Holder(widths=left, heights=bottom)

        self.corner_cache[
            CornerKey(tile.x, tile.y, CornerEnum.RB)] = \
            Holder(widths=left, heights=top)

    def get_wh(self, corner, left, right, top, bottom):
        if corner == CornerEnum.LT:
            return random.choice(right), random.choice(bottom)
        if corner == CornerEnum.LB:
            return random.choice(right), random.choice(top)
        if corner == CornerEnum.RT:
            return random.choice(left), random.choice(bottom)
        if corner == CornerEnum.RB:
            return random.choice(left), random.choice(top)
