import random

import api.level_generator.geomerty as geometry
from api.level_generator.models import LevelConfig, Room


class HotlineGenerator:
    def generate(self, level_config: LevelConfig):
        """
        Generates a level graph
        :param level_config:
        :return:
        """

        first_room = self._make_first_room(level_config)
        rooms = [first_room]
        for _ in range(level_config.room_number - 1):
            room = self._place_room(level_config, rooms)
            rooms.append(room)
        return rooms

    def _place_room(self, level_config: LevelConfig, rooms: list):
        # support only underlap
        # pick a room from the rooms list
        target_room = self._pick_room(rooms)
        # TODO make size
        width = random.randint(int(level_config.max_width / 12) + 1,
                               int(level_config.max_width / 6) + 1)
        height = random.randint(int(level_config.max_height / 12) + 1,
                                int(level_config.max_height / 6) + 1)
        # only create rooms that underlap with ONLY one other room
        other_rooms = list(rooms)
        other_rooms.remove(target_room)
        new_room = self._make_new_room(target_room, other_rooms,
                                       level_config,
                                       width, height)

        target_room.underlap_room(new_room)
        target_room.connect(new_room)

        return new_room

    def _pick_room(self, rooms):
        # TODO a more intelligent algorithm
        return random.choice(rooms)

    def _make_first_room(self, level_config: LevelConfig):
        x, y = int(level_config.max_width / 2), \
               int(level_config.max_height / 2)
        width = random.randint(int(level_config.max_width / 12) + 1,
                               int(level_config.max_width / 6) + 1)
        height = random.randint(int(level_config.max_height / 12) + 1,
                                int(level_config.max_height / 6) + 1)
        return Room(bounds=geometry.Rect.make_rect((x, y), width, height))

    def _make_new_room(self, target_room, rooms, level_config, width, height):
        # generate a room that underlaps the target_room
        # and intersects with no other room from rooms

        # pick a random point inside target room, determine what corner is that
        # generate bounds
        # check that the room doesn't intersect with other rooms

        while True:
            point = geometry.make_point_inside(target_room.bounds)
            # TODO WHATTHEFUCK, it obviously has to be redone
            # it's here just so I could run the code
            attempts = 0
            while attempts < 10:
                corner = geometry.CornerEnum.random()
                try:
                    origin = geometry.transform_origin(
                        point, width, height, corner)
                    bounds = geometry.Rect.make_rect(origin, width, height)
                    attempts += 1
                except ValueError:
                    continue
                else:
                    if all(not geometry.find_common_rect(room.bounds, bounds)
                           for room in rooms):
                        return Room(bounds)
