from unittest import TestCase

from api.level_generator.generator import Generator
from api.level_generator.geometry import Rect


class TestScanner(TestCase):
    def setUp(self):
        self.generator = Generator(50, 50)
        self.map = self.generator.map
        # self.room = self.generator._make_first_room()

    def test_horizontal_scan(self):
        # add room
        rect = Rect.make_rect((10, 10,), 20, 30)
        room = self.generator._place_room_above(rect)
        tile = self.map.get(17, 20)
        left, right = self.map.calculate_room_widths(tile, room)
        expected_left = [3, 4, 5, 6] + list(range(9, 18))
        expected_right = list(range(3, 12)) + list(range(14, 50 - 17))
        # [0,9] + [12, 15]
        self.assertEqual(expected_left, left)
        self.assertEqual(expected_right, right)

    def test_horizontal_scan_left_close(self):
        # add room
        rect = Rect.make_rect((10, 10,), 20, 30)
        room = self.generator._place_room_above(rect)
        tile = self.map.get(12, 20)
        left, right = self.map.calculate_room_widths(tile, room)
        expected_left = list(range(4, 13))
        expected_right = list(range(3, 17)) + list(range(19, 50 - 12))
        # [0,9] + [12, 15]
        self.assertEqual(expected_left, left)
        self.assertEqual(expected_right, right)

    def test_horizontal_scan_right_close(self):
        # add room
        rect = Rect.make_rect((10, 10,), 20, 30)
        room = self.generator._place_room_above(rect)
        tile = self.map.get(27, 20)
        left, right = self.map.calculate_room_widths(tile, room)
        expected_left = list(range(3, 17)) + list(range(19, 28))
        expected_right = list(range(4, 50 - 27))
        # [0,9] + [12, 15]
        self.assertEqual(expected_left, left)
        self.assertEqual(expected_right, right)

    # def test_recalculate(self):
    #     # add room
    #     rect = Rect.make_rect((10, 10,), 20, 30)
    #     room = self.generator._place_room_above(rect)
    #     self.generator.recalculate_potential_corners(room)
    #
    #     # rect = Rect.make_rect((17, 20,), 30, 30)
    #     room2 = self.generator._make_new_room(None)
    #     # room2 = self.generator._place_room_above(rect)
    #     self.generator.recalculate_potential_corners(room2)
    #     self.generator.recalculate_potential_corners(room)
    #     # tile = self.map.get(17, 20)
    #     # left, right = self.map.calculate_room_widths(tile, room)
    #     # expected_left = [3, 4, 5, 6] + list(range(9, 18))
    #     # expected_right = list(range(3, 12)) + list(range(14, 50 - 17))
    #     # # [0,9] + [12, 15]
    #     # self.assertEqual(expected_left, left)
    #     # self.assertEqual(expected_right, right)
