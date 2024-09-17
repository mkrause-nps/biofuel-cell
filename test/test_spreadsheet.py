#!/usr/bin/env python3
import os
import unittest

import numpy as np
import pandas as pd
from src.spreadsheet import Spreadsheet


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.excel_filename = os.path.abspath("./data/some_data.xlsx")

    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

    def test_constructor(self):
        spreadsheet = Spreadsheet(self.excel_filename)
        self.assertEqual(f'Spreadsheet instance: {self.excel_filename}', str(spreadsheet))

    def test_getter(self):
        spreadsheet = Spreadsheet(self.excel_filename)
        self.assertEqual(self.excel_filename, spreadsheet.excel_filename)

    def test_setter(self):
        spreadsheet = Spreadsheet(self.excel_filename)
        with self.assertRaises(AttributeError):
            spreadsheet.excel_filename = "/home/bob/my_new_excelfile.xlsx"

    def test_getter_sheet_names(self):
        spreadsheet = Spreadsheet(self.excel_filename)
        expected = ('tab_00', 'tab_01', 'tab_02')
        observed = spreadsheet.sheet_names
        self.assertEqual(expected, observed)

    def test_setter_sheet_names(self):
        tab_names = ('foo0', 'foo1')
        spreadsheet = Spreadsheet(self.excel_filename)
        with self.assertRaises(AttributeError):
            spreadsheet.sheet_names = tab_names

    def test_get_averages_easy(self):
        spreadsheet = Spreadsheet(self.excel_filename)
        averages = spreadsheet.get_averages(tab_name='tab_00')
        expected = {
            'injection': [1, 2, 3, 4],
            'avg. R (kOhm)': [1848.0, 19.66667, 123.666667, 9.40]
        }
        expected = pd.DataFrame(expected)
        pd.testing.assert_frame_equal(averages, expected)


    def test_get_stdevs_easy(self):
        spreadsheet = Spreadsheet(self.excel_filename)
        stdevs = spreadsheet.get_stdevs(tab_name='tab_00')
        print(stdevs)

    def test_get_average_tab_name_not_in_sheet(self):
        spreadsheet = Spreadsheet(self.excel_filename)
        with self.assertRaises(ValueError):
            spreadsheet.get_averages()

    def test_get_num_observations(self):
        spreadsheet = Spreadsheet(self.excel_filename)
        obs = spreadsheet.get_num_observations(tab_name='tab_00')
        expected = np.array([3, 3, 3, 3])
        np.testing.assert_array_equal(obs, expected)

    def test_get_average_of_averages(self):
        spreadsheet = Spreadsheet(self.excel_filename)
        print(spreadsheet.get_average_of_averages(tab_name='tab_00'))


if __name__ == '__main__':
    unittest.main()
