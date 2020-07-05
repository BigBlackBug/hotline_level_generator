from typing import List

from PIL import Image, ImageDraw

from api.level_generator.models import Room, Map

TILE_SIZE_PX = 10


def _draw_mesh(idraw, width, height):
    for x in range(0, width, TILE_SIZE_PX):
        idraw.line((x, 0, x, height), fill='green')
    for y in range(0, height, TILE_SIZE_PX):
        idraw.line((0, y, width, y), fill='green')


def make_image(map: Map, rooms: List[Room]):
    img = Image.new('RGBA', (map.width * TILE_SIZE_PX,
                             map.height * TILE_SIZE_PX),
                    'blue')
    idraw = ImageDraw.Draw(img)
    _draw_mesh(idraw, img.width, img.height)
    for room in rooms:
        _draw_room(room, idraw)
    return img


def _draw_room(room, idraw):
    for wall in room.walls:
        fill = 'red' if wall.potential_door else 'white'
        print(f"wall {wall.tile.x, wall.tile.y}")
        _draw_tile(wall.tile, idraw, fill=fill)


def _draw_tile(tile, idraw, fill):
    # for
    dimensions = [tile.x * TILE_SIZE_PX,
                  tile.y * TILE_SIZE_PX,
                  (tile.x + 1) * TILE_SIZE_PX,
                  (tile.y + 1) * TILE_SIZE_PX]
    # print(f'rect {dimensions}')
    idraw.rectangle(dimensions, outline=fill)
