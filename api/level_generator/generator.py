import random

from api.level_generator import geometry
from api.level_generator.geometry import Rect
from api.level_generator.models import Room, Map

_MAX_ATTEMPTS = 10


class Generator:
    def __init__(self, map_width, map_height):
        self.map = Map((map_width, map_height))

    def generate(self, room_number):
        """
        Generates a level graph
        :param level_config:
        :return: list of Rooms
        """
        first_room = self._make_first_room()
        rooms = [first_room]
        for _ in range(room_number - 1):
            room = self._add_new_room(rooms)
            rooms.append(room)
        return rooms

    def _make_first_room(self):
        x, y = int(self.map.width / 2), \
               int(self.map.height / 2)
        width = random.randint(int(self.map.width / 8) + 1,
                               int(self.map.width / 3) + 1)
        height = random.randint(int(self.map.height / 8) + 1,
                                int(self.map.height / 3) + 1)
        start_tile = self.map.get(x, y)
        return self._place_room_above(start_tile, width, height)

    def _place_room_above(self, start_tile, width, height):
        new_room = Room(Rect.make_rect(
            (start_tile.x, start_tile.y), width, height))
        for tile in self.map.next_tiles(
                start_tile.x, start_tile.y, width, height):
            if tile.lies_on_rect_bounds(
                    (start_tile.x, start_tile.y), width, height):
                bottom_room = tile.room
                tile.clear()

                is_corner = tile.is_corner(
                    (start_tile.x, start_tile.y), width, height)
                new_room.add_wall(tile, bottom_room, is_corner)
            else:
                tile.clear()
                new_room.add_tile(tile)

        return new_room

    def _add_new_room(self, rooms: list):
        target_room = self._pick_room(rooms)
        # TODO a better random, this is temporary BS
        width = random.randint(int(self.map.width / 8) + 1,
                               int(self.map.width / 3) + 1)
        height = random.randint(int(self.map.height / 8) + 1,
                                int(self.map.height / 3) + 1)
        # create rooms that underlap with ONLY one other room
        other_rooms = list(rooms)
        other_rooms.remove(target_room)
        above_room = self._make_new_room(width, height, target_room,
                                         other_rooms)

        return above_room

    def _pick_room(self, rooms):
        # TODO a more intelligent algorithm
        return random.choice(rooms)

    def _make_new_room(self, width, height, target_room, other_rooms, ):
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
        while True:
            point = geometry.make_point_inside(target_room.bounds)

            attempts = 0
            while attempts < _MAX_ATTEMPTS:
                corner = geometry.CornerEnum.random()
                try:
                    origin = geometry.transform_origin(
                        point, width, height, corner)
                    bounds = geometry.Rect.make_rect(origin, width, height)
                except ValueError:
                    # in case make_rect fails
                    continue
                else:
                    if all(not geometry.find_common_rect(room.bounds, bounds)
                           for room in other_rooms):
                        start_tile = self.map.get(point[0], point[1])
                        return self._place_room_above(start_tile, width, height)
                attempts += 1
