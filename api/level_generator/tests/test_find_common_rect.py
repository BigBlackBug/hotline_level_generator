from unittest import TestCase

from api.level_generator.geomerty import Rect, Line, find_common_rect


class TestFindCommonRect(TestCase):
    def test_find_common_rect_disjoint(self):
        bounds_one = Rect(Line((5, 1), (7, 1)), Line((7, 1), (7, 3)),
                          Line((5, 3), (7, 3)), Line((5, 1), (5, 3)))
        bounds_two = Rect(Line((1, 3), (3, 3)), Line((3, 3), (3, 6)),
                          Line((1, 6), (3, 6)), Line((1, 3), (1, 6)))
        self.assertIsNone(find_common_rect(bounds_one, bounds_two))

    def test_find_common_side_inside(self):
        bounds_one = Rect(Line((5, 1), (7, 1)), Line((7, 1), (7, 4)),
                          Line((5, 4), (7, 4)), Line((5, 1), (5, 4)))
        bounds_two = Rect(Line((1, 3), (9, 3)), Line((9, 3), (9, 6)),
                          Line((1, 6), (9, 6)), Line((1, 3), (1, 6)))
        result = find_common_rect(bounds_one, bounds_two)
        common_rect = Rect(Line((5, 3), (7, 3)), Line((7, 3), (7, 4)),
                           Line((5, 4), (7, 4)), Line((5, 3), (5, 4)))
        self.assertEquals(result, common_rect)

    def test_find_common_side_touches_corner(self):
        bounds_two = Rect(Line((1, 1), (2, 1)), Line((2, 1), (2, 2)),
                          Line((1, 2), (2, 2)), Line((1, 1), (1, 2)))
        bounds_one = Rect(Line((2, 2), (3, 2)), Line((3, 2), (3, 3)),
                          Line((2, 3), (3, 3)), Line((2, 2), (2, 3)))
        result = find_common_rect(bounds_one, bounds_two)
        self.assertIsNone(result)

    # TODO more tests
    def test_find_common_side_intersects_lt(self):
        raise NotImplementedError("Not implemented")

    def test_find_common_side_intersects_rt(self):
        bounds_one = Rect(Line((1, 2), (4, 2)), Line((4, 2), (4, 5)),
                          Line((1, 5), (4, 5)), Line((1, 2), (1, 5)))
        bounds_two = Rect(Line((3, 1), (7, 1)), Line((7, 1), (7, 3)),
                          Line((3, 3), (7, 3)), Line((3, 1), (3, 3)))
        result = find_common_rect(bounds_one, bounds_two)
        common_rect = Rect(Line((3, 2), (4, 2)), Line((4, 2), (4, 3)),
                           Line((3, 3), (4, 3)), Line((3, 2), (3, 3)))
        self.assertEquals(result, common_rect)

    def test_find_common_side_intersects_rb(self):
        raise NotImplementedError("Not implemented")

    def test_find_common_side_intersects_lb(self):
        raise NotImplementedError("Not implemented")
