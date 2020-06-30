import random
from typing import List

import api.level_generator.geomerty as geometry
from api.level_generator.models import LevelConfig, Room

_MAX_ATTEMPTS = 10


def generate(level_config: LevelConfig) -> List[Room]:
    """
    Generates a level graph
    :param level_config:
    :return: list of Rooms
    """

    first_room = _make_first_room(level_config)
    rooms = [first_room]
    for _ in range(level_config.room_number - 1):
        room = _add_new_room(level_config, rooms)
        rooms.append(room)
    return rooms


def _add_new_room(level_config: LevelConfig, rooms: list):
    target_room = _pick_room(rooms)
    # TODO a better random, this is temporary BS
    width = random.randint(int(level_config.max_width / 12) + 1,
                           int(level_config.max_width / 6) + 1)
    height = random.randint(int(level_config.max_height / 12) + 1,
                            int(level_config.max_height / 6) + 1)
    # create rooms that underlap with ONLY one other room
    other_rooms = list(rooms)
    other_rooms.remove(target_room)
    new_room = _make_new_room(width, height, target_room, other_rooms,
                              level_config)

    target_room.underlap_room(new_room)
    target_room.connect(new_room)

    return new_room


def _pick_room(rooms):
    # TODO a more intelligent algorithm
    return random.choice(rooms)


def _make_first_room(level_config: LevelConfig):
    x, y = int(level_config.max_width / 2), \
           int(level_config.max_height / 2)
    width = random.randint(int(level_config.max_width / 12) + 1,
                           int(level_config.max_width / 6) + 1)
    height = random.randint(int(level_config.max_height / 12) + 1,
                            int(level_config.max_height / 6) + 1)
    return Room(bounds=geometry.Rect.make_rect((x, y), width, height))


def _make_new_room(width, height, target_room, other_rooms, level_config, ):
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
    # TODO WHATTHEFUCK, this obviously has to be redone
    # it's here just so I could run the code
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
                    return Room(bounds)
            attempts += 1
