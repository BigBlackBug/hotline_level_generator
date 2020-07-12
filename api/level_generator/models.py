from api.level_generator.geometry import Rect
# from api.level_generator import image_generator as ig
MIN_CORRIDOR_SIZE = 1


class Tile:
    def __init__(self, coords: tuple):
        if len(coords) != 2:
            raise ValueError("coords should be a tuple of size 2")
        self.x, self.y = coords
        self.wall = None
        self.room = None

    def __str__(self):
        return f"T({self.x}, {self.y}), wall({self.wall is not None}), " \
               f"room({self.room is not None})"

    def clear(self):
        if self.wall:
            self.wall.clear(self)
            self.wall = None
        if self.room:
            self.room.drop_tile(self)
            self.room = None

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return super().__hash__()

    def lies_on_rect_bounds(self, origin, width, height):
        x, y = origin
        return (x <= self.x <= x + width - 1 and (
                self.y == y or self.y == y + height - 1)) or \
               (y <= self.y <= y + height - 1 and (
                       self.x == x or self.x == x + width - 1))

    def is_corner(self, origin, width, height):
        x, y = origin
        return self.x == x and self.y == y or \
               self.x == x and self.y == y + height - 1 or \
               self.x == x + width - 1 and self.y == y or \
               self.x == x + width - 1 and self.y == y + height - 1

    def has_neighboring_walls(self, map):
        for x in range(self.x - 1, self.x + 2):
            for y in range(self.y - 1, self.y + 2):
                tile = map.get(x, y)
                if tile and tile != self and tile.wall:
                    return True
        return False


class Wall:
    def __init__(self, tile):
        self._room_one = None
        self._room_two = None
        self.tile = tile
        self.is_corner = False

    def clear(self, tile):
        if self.room_one:
            self.room_one.drop_tile(tile)
        if self.room_two:
            self.room_two.drop_tile(tile)

    @property
    def room_one(self):
        return self._room_one

    @room_one.setter
    def room_one(self, room):
        if room:
            room.walls.add(self)
        self._room_one = room

    @property
    def room_two(self):
        return self._room_two

    @room_two.setter
    def room_two(self, room):
        if room:
            room.walls.add(self)
        self._room_two = room

    @property
    def potential_door(self):
        return self.room_one and self.room_two and not self.is_corner

    def __eq__(self, other):
        return id(self) == id(other)

    def __hash__(self):
        return super().__hash__()

    def __str__(self):
        return f"Wall@({self.tile.x, self.tile.y})"


class Room:
    def __init__(self, bounds: Rect):
        self.walls = set()
        self.tiles = set()
        self.bounds = bounds

    def drop_tile(self, tile):
        self.walls.discard(tile.wall)
        self.tiles.discard(tile)

    def add_tile(self, tile):
        tile.room = self
        self.tiles.add(tile)

    def add_wall(self, tile, other_room=None, is_corner=False):
        new_wall = Wall(tile)

        new_wall.room_one = self
        new_wall.room_two = other_room
        new_wall.is_corner = is_corner

        tile.wall = new_wall


class Map:
    def __init__(self, size):
        self.width, self.height = size
        map = []
        for y in range(size[1]):
            row = []
            for x in range(size[0]):
                row.append(Tile((y, x)))
            map.append(row)
        self.map = map

    def get(self, x, y):
        if x < 0 or x > self.width - 1 or y < 0 or y > self.height - 1:
            return None
        return self.map[x][y]

    def next_tiles(self, start_x, start_y, width, height):
        used_tiles = set()
        for x in range(start_x, start_x + width):
            for y in range(start_y, start_y + height):
                tile = self.get(x, y)
                if tile and tile not in used_tiles:
                    used_tiles.add(tile)
                    yield tile

    def calculate_room_widths(self, tile, room):
        """
        Returns potential widths of a new room inside ROOM starting
        from tile TILE
        :param tile:
        :param room:
        :return:
        """
        origin = (tile.x, tile.y)
        # left
        widths = self._scan_h(origin, x_from=tile.x - 1, x_to=0, room=room)

        # right
        widths2 = self._scan_h(origin, x_from=tile.x + 1, x_to=self.width,
                               room=room)
        # print(f"for tile {tile} - {widths},{widths2}")
        return widths, widths2

    def calculate_room_heights(self, tile, room):
        origin = (tile.x, tile.y)
        # top
        heights = self._scan_v(origin, y_from=tile.y - 1, y_to=0, room=room)

        # bot
        heights2 = self._scan_v(origin, y_from=tile.y + 1, y_to=self.height,
                                room=room)
        # print(f"for tile {tile} - {heights},{heights2}")
        return heights, heights2

    def _scan_h(self, origin, x_from, x_to, room):
        dir = 1 if x_to > x_from else -1
        second_default = max(0, x_to - 1)
        first_match = None
        second_match = None
        for x in range(x_from, x_to, dir):
            next_tile = self.get(x, origin[1])
            if not first_match:
                if next_tile.wall and (next_tile.wall.room_one == room
                                       or next_tile.wall.room_two == room):
                    first_match = next_tile
            else:
                if next_tile.wall:
                    second_match = next_tile
                    break
        second_match = second_match.x if second_match else second_default
        # return first_match, second_match
        widths = []
        # for right +1 to to
        widths.extend(
            range(MIN_CORRIDOR_SIZE + 1 + 1,
                  dir * (first_match.x - origin[0]) - MIN_CORRIDOR_SIZE + 1))
        # for right +1 to from
        widths.extend(
            range(dir * (first_match.x - origin[0]) + MIN_CORRIDOR_SIZE + 1,
                  dir * (second_match - origin[0]) + 1))
        return widths

    def _scan_v(self, origin, y_from, y_to, room):
        dir = 1 if y_to > y_from else -1
        second_default = max(0, y_to - 1)
        first_match = None
        second_match = None
        for y in range(y_from, y_to, dir):
            next_tile = self.get(origin[0], y)
            if not first_match:
                if next_tile.wall and (next_tile.wall.room_one == room or
                                       next_tile.wall.room_two == room):
                    first_match = next_tile
            else:
                if next_tile.wall:
                    second_match = next_tile
                    break
        second_match = second_match.y if second_match else second_default
        # return first_match, second_match
        heights = []
        # for right +1 to to
        heights.extend(
            range(MIN_CORRIDOR_SIZE + 1 + 1,
                  dir * (first_match.y - origin[1]) - MIN_CORRIDOR_SIZE + 1))
        # for right +1 to from
        heights.extend(
            range(dir * (first_match.y - origin[1]) + MIN_CORRIDOR_SIZE + 1,
                  dir * (second_match - origin[1]) + 1))
        return heights
