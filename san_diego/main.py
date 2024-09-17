#!/usr/bin/env python3
import os
from src.utility import _Utility
from src.spreadsheet import Spreadsheet
from src.weighted_average import WeightedAverage


def main():
    data_dir = _Utility.get_user_data_dir_path()
    project_dir = 'chips_for_san_diego'
    excel_filename = os.path.join(data_dir, project_dir, 'resistance_zoa.xlsx')
    spreadsheet = Spreadsheet(excel_filename=excel_filename)

    for sheet_name in spreadsheet.sheet_names:
        print(f'\nsheet_name: {sheet_name}:')
        df = spreadsheet.get_dataframe(tab_name=sheet_name)
        weighted_average = WeightedAverage(df=df, num_obs=spreadsheet.NUMBER_OF_SAMPLES)
        print(weighted_average.get_weighted_average())


if __name__ == '__main__':
    main()
