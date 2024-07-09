#!/usr/bin/env python3
import unittest
from src.utility import _Utility


class TestUtility(unittest.TestCase):
    def test_get_user_data_dir_path(self):
        expected = '/home/mkrause/data/biofuel-cell'
        actual = _Utility.get_user_data_dir_path()
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
