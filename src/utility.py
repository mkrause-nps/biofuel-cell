#!/usr/bin/env python3
import pandas as pd

class Utility(object):

    @staticmethod
    def remove_whitespace_from_pd_header(columns: pd.DataFrame.columns) -> pd.DataFrame:
        return columns.str.replace(' ', '')

    @staticmethod
    def remove_undesired_symbols_from_pd_header(columns: pd.DataFrame.columns) -> pd.DataFrame:
        return columns.str.replace('%', 'percent_')
