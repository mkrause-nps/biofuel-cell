#!/usr/bin/env python3
from src.utility import _Utility


class Spreadsheet:
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

    def __str__(self):
        return f"Spreadsheet instance: {self.__excel_filename}"



if __name__ == '__main__':
    pass
