#!/usr/bin/env python3
import os
import numpy as np
import pandas as pd
from src.i_spreadsheet import ISpreadsheet


class Spreadsheet(ISpreadsheet):
    """Spreadsheet for crescent chip resistance measurements."""

    NUMBER_OF_SAMPLES: int = (
        100  # samples taken by the multimeter to produce an average value
    )

    def __init__(self, excel_filename: str):
        self.__excel_filename = os.path.abspath(excel_filename)
        excel_file = pd.ExcelFile(self.__excel_filename)
        self.__sheet_names = excel_file.sheet_names

    @property
    def excel_filename(self):
        return self.__excel_filename

    @excel_filename.setter
    def excel_filename(self, excel_filename: str):
        raise AttributeError("excel_filename attribute is read-only")

    @property
    def sheet_names(self) -> tuple:
        return tuple(self.__sheet_names)

    @sheet_names.setter
    def sheet_names(self, sheet_names: tuple):
        raise AttributeError("sheet_names attribute is read-only")

    def get_num_observations(self, tab_name: str = "Sheet1") -> np.ndarray:
        """Return array of size n, where n is the number of experiments."""
        if not self.__is_tab_name_in_file(tab_name=tab_name):
            raise ValueError(f"tab name {tab_name} is not file {self.excel_filename}")
        df = pd.read_excel(self.__excel_filename, sheet_name=tab_name)
        num_rows = df.shape[0]
        return np.array([self.NUMBER_OF_SAMPLES] * num_rows)

    def get_dataframe(self, tab_name: str = "Sheet1") -> pd.DataFrame:
        return pd.read_excel(self.__excel_filename, sheet_name=tab_name)

    def _get_averages(self, tab_name: str = "Sheet1") -> pd.DataFrame:
        """Return a dataframe containing averages for each experiment in sheet."""
        if not self.__is_tab_name_in_file(tab_name=tab_name):
            raise ValueError(f"tab name {tab_name} is not file {self.excel_filename}")
        df = pd.read_excel(self.__excel_filename, sheet_name=tab_name)
        column_names = self.__get_column_names(df=df)
        return df.groupby(column_names[0])[column_names[2]].mean().reset_index()

    def _get_stdevs(self, tab_name: str = "Sheet1") -> pd.DataFrame:
        """Return a dataframe containing standard deviations for each experiment in sheet."""
        if not self.__is_tab_name_in_file(tab_name=tab_name):
            raise ValueError(f"tab name {tab_name} is not file {self.excel_filename}")
        df = pd.read_excel(self.__excel_filename, sheet_name=tab_name)
        column_names = self.__get_column_names(df=df)
        return df.groupby(column_names[0])[column_names[3]].mean().reset_index()

    @staticmethod
    def __get_weighted_mean(
        averages: np.ndarray, num_observations: np.ndarray
    ) -> np.ndarray:
        return np.sum(num_observations * averages) / np.sum(num_observations)

    def __get_column_values(self, df: pd.DataFrame) -> np.ndarray:
        column_name = self.__get_column_names(df=df)[1]
        return df[column_name].to_numpy()

    @staticmethod
    def __get_column_names(df: pd.DataFrame) -> tuple:
        return tuple(df.columns)

    def __is_tab_name_in_file(self, tab_name: str) -> bool:
        return tab_name in self.__sheet_names

    def __str__(self):
        return f"Spreadsheet instance: {self.__excel_filename}"
