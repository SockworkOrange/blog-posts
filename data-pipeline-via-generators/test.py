from main import filter_numbers, fixed_event_window, fold_median, fold_sum
import unittest


class TestPipeline(unittest.TestCase):
    def test_filter_numbers(self):
        self.assertEqual(list(filter_numbers(range(1, 8), lambda x: x > 5)), list(range(6, 8)))

    def test_fixed_event_window(self):
        self.assertEqual(list(fixed_event_window(range(1, 7), 3)), [[1, 2, 3], [4, 5, 6]])

    def test_fold_sum(self):
        self.assertEqual(list(fold_sum([range(1, 4)])), [6])

    def test_fold_median(self):
        self.assertEqual(list(fold_median([range(1, 6)])), [3])