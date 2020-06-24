from typing import List

from PIL import Image, ImageDraw

from api.level_generator.models import LevelConfig, Room

TILE_SIZE_PX = 1


def _draw_mesh(idraw, width, height):
    for x in range(0, width, TILE_SIZE_PX):
        idraw.line((x, 0, x, height), fill='green')
    for y in range(0, height, TILE_SIZE_PX):
        idraw.line((0, y, width, y), fill='green')


def make_image(level_config: LevelConfig, rooms: List[Room]):
    img = Image.new('RGBA', (level_config.max_width * TILE_SIZE_PX,
                             level_config.max_height * TILE_SIZE_PX),
                    'blue')
    idraw = ImageDraw.Draw(img)
    _draw_mesh(idraw, img.width, img.height)
    for room in rooms:
        _draw_room(room, idraw)
    img.save('rectangle.png')


def _draw_room(room, idraw):
    for wall in room.walls:
        fill = 'red' if wall.shared_wall else 'white'
        _draw_wall(wall.line, idraw, fill=fill)


def _draw_wall(line, idraw, fill):
    # for
    if line.is_horizontal:
        idraw.rectangle((line.start[0] * TILE_SIZE_PX,
                         line.start[1] * TILE_SIZE_PX,
                         (line.end[0]+1) * TILE_SIZE_PX,
                         line.end[1] + TILE_SIZE_PX),
                        fill=fill, outline=None)
    elif line.is_vertical:
        idraw.rectangle((line.start[0] * TILE_SIZE_PX,
                         line.start[1] * TILE_SIZE_PX,
                         line.end[0] + TILE_SIZE_PX,
                         (line.end[1]+1) * TILE_SIZE_PX),
                        fill=fill, outline=None)
    # idraw.line((line.start[0], line.start[1], line.end[0],
    #             line.end[1]), fill=fill)
