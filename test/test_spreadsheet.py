#!/usr/bin/env python3
import unittest
from src.spreadsheet import Spreadsheet


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.excel_filename = "/home/alice/data/my_excelfile.xlsx"

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



if __name__ == '__main__':
    unittest.main()
