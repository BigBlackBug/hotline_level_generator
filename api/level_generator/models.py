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


class Room:
    def __init__(self):
        self.walls = set()
        self.tiles = set()

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
        return self.map[x][y]

    def next_tiles(self, start_x, start_y, width, height):
        used_tiles = set()
        for x in range(start_x, start_x + width):
            for y in range(start_y, start_y + height):
                tile = self.get(x, y)
                if tile not in used_tiles:
                    used_tiles.add(tile)
                    yield tile
