#!/usr/bin/env python3
from src.i_spreadsheet import ISpreadsheet
from src.utility import _Utility


class Spreadsheet(ISpreadsheet):
    def __init__(self, excel_filename: str):
        if not _Utility.is_absolute_path(excel_filename):
            raise ValueError(f'"{excel_filename}" is not absolute path')
        self.__excel_filename = excel_filename

    @property
    def excel_filename(self):
        return self.__excel_filename

    @excel_filename.setter
    def excel_filename(self, excel_filename: str):
        raise AttributeError('excel_filename attribute is read-only')

    def get_average(self, tab: str='Sheet1') -> float:
        pass

    def get_stdev(self, tab: str='Sheet1') -> float:
        pass

    def __str__(self):
        return f"Spreadsheet instance: {self.__excel_filename}"

