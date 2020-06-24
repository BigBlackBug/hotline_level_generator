from unittest import TestCase

from api.level_generator.geomerty import Line


class TestLine(TestCase):
    def test_lines_intersect_horizontal(self):
        line_1 = Line((1, 5), (4, 5))
        line_2 = Line((2, 5), (3, 5))
        result = line_1.split_via(line_2)
        expected = [Line((1, 5), (2, 5)), Line((2, 5), (3, 5)),
                    Line((3, 5), (4, 5))]
        self.assertEquals(result, expected)

    def test_lines_equal(self):
        line_1 = Line((1, 5), (4, 5))
        line_2 = Line((1, 5), (4, 5))
        result = line_1.split_via(line_2)
        expected = [Line((1, 5), (4, 5))]
        self.assertEquals(result, expected)

    def test_lines_same_axis_no_intersection_horizontal(self):
        line_1 = Line((1, 5), (4, 5))
        line_2 = Line((5, 5), (8, 5))
        result = line_1.split_via(line_2)
        self.assertEquals(result, [])

    def test_lines_intersect_vertical(self):
        line_1 = Line((5, 0), (5, 6))
        line_2 = Line((5, 4), (5, 6))
        result = line_1.split_via(line_2)
        expected = [Line((5, 0), (5, 4)), Line((5, 4), (5, 6))]
        self.assertEquals(result, expected)

    def test_lines_parallel_not_intersect_horizontal(self):
        line_1 = Line((1, 5), (4, 5))
        line_2 = Line((2, 3), (5, 3))
        result = line_1.split_via(line_2)
        self.assertEquals(len(result), 0)

    def test_lines_parallel_not_intersect_vertical(self):
        line_1 = Line((5, 0), (5, 3))
        line_2 = Line((2, 2), (2, 5))
        result = line_1.split_via(line_2)
        self.assertEquals(len(result), 0)

    def test_lines_not_parallel(self):
        line_1 = Line((5, 0), (5, 3))
        line_2 = Line((2, 3), (5, 3))
        result = line_1.split_via(line_2)
        self.assertEquals(len(result), 0)
