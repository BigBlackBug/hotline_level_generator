from unittest import TestCase

from api.level_generator.generator import Generator


class TestPlaceRoom(TestCase):
    def setUp(self):
        self.generator = Generator(50, 50)
        self.map = self.generator.map

    def test_place_first(self):
        start_tile = self.map.get(1, 2)
        width = 10
        height = 7
        room = self.generator._place_room_above(start_tile, width, height)
        for x in range(start_tile.x, start_tile.x + width):
            for y in range(start_tile.y, start_tile.y + height):
                tile = self.map.get(x, y)
                if x == start_tile.x or x == start_tile.x + width - 1 or \
                        y == start_tile.y or y == start_tile.y + height - 1:
                    self.assertIsNotNone(tile.wall)
                    self.assertEqual(tile.wall.room_one, room)
                    self.assertIn(tile.wall, room.walls)
                else:
                    self.assertIsNone(tile.wall)
                    self.assertEqual(tile.room, room)
                    self.assertIn(tile, room.tiles)

    def test_place_second(self):
        br_x, br_y = 1, 2
        br_w, br_h = 10, 7
        below_room = self.generator._place_room_above(self.map.get(br_x, br_y),
                                                      br_w, br_h)

        ar_x, ar_y = 7, 5
        start_tile = self.map.get(ar_x, ar_y)
        ar_width = 12
        ar_height = 9
        above_room = self.generator._place_room_above(start_tile, 12, 9)
        for x in range(start_tile.x, start_tile.x + ar_width):
            for y in range(start_tile.y, start_tile.y + ar_height):
                tile = self.map.get(x, y)
                # joint walls
                if ar_x <= x <= br_x + br_w - 1 and y == ar_y or \
                        x == ar_x and ar_y <= y <= br_y + br_h - 1:
                    self.assertEqual(tile.wall.room_one, above_room)
                    self.assertIn(tile.wall, above_room.walls)
                    if tile.wall.room_two:
                        self.assertEqual(tile.wall.room_two, below_room)
                        self.assertIn(tile.wall, below_room.walls)
                    print(f"Joint wall {x, y}")
                elif br_x + br_w <= x < ar_x + ar_width and y == ar_y or \
                        x == ar_x and br_y + br_h <= y < ar_y + ar_height or \
                        x == ar_x + ar_width - 1 and ar_y <= y < ar_y + ar_height or \
                        y == ar_y + ar_height - 1 and ar_x <= x < ar_x + ar_width:
                    print(f"Above room wall {x, y}")
                    self.assertIsNotNone(tile.wall)
                    self.assertEqual(tile.wall.room_one, above_room)
                else:
                    print(f"above room tile {x, y}")
                    self.assertIsNone(tile.wall)
                    self.assertEqual(tile.room, above_room)
                    self.assertNotIn(tile.wall, below_room.walls)
                    self.assertNotIn(tile, below_room.tiles)

    def test_is_a_new_room(self):
        coords = (0, 0)
        width = 3
        height = 3
        self.assertTrue(self.map.get(0, 0).lies_on_rect_bounds(
            coords, width, height))
        self.assertTrue(self.map.get(0, 1).lies_on_rect_bounds(
            coords, width, height))
        self.assertTrue(self.map.get(0, 2).lies_on_rect_bounds(
            coords, width, height))

        self.assertTrue(self.map.get(1, 0).lies_on_rect_bounds(
            coords, width, height))
        self.assertFalse(self.map.get(1, 1).lies_on_rect_bounds(
            coords, width, height))
        self.assertTrue(self.map.get(1, 2).lies_on_rect_bounds(
            coords, width, height))

        self.assertTrue(self.map.get(2, 0).lies_on_rect_bounds(
            coords, width, height))
        self.assertTrue(self.map.get(2, 1).lies_on_rect_bounds(
            coords, width, height))
        self.assertTrue(self.map.get(2, 2).lies_on_rect_bounds(
            coords, width, height))
