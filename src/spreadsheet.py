#!/usr/bin/env python3
import os
from typing import Tuple
import numpy as np
import pandas as pd
from src.i_spreadsheet import ISpreadsheet


class Spreadsheet(ISpreadsheet):

    NUMBER_OF_SAMPLES: int = 100  # samples taken by the multimeter to produce an average value

    def __init__(self, excel_filename: str):
        self.__excel_filename = os.path.abspath(excel_filename)
        excel_file = pd.ExcelFile(excel_filename)
        self.__sheet_names = excel_file.sheet_names

    @property
    def excel_filename(self):
        return self.__excel_filename

    @excel_filename.setter
    def excel_filename(self, excel_filename: str):
        raise AttributeError('excel_filename attribute is read-only')

    @property
    def sheet_names(self) -> tuple:
        return tuple(self.__sheet_names)

    @sheet_names.setter
    def sheet_names(self, sheet_names: tuple):
        raise AttributeError('sheet_names attribute is read-only')

    def _get_averages(self, tab_name: str= 'Sheet1') -> pd.DataFrame:
        """Return a dataframe containing averages for each experiment in sheet."""
        if not self.__is_tab_name_in_file(tab_name=tab_name):
            raise ValueError(f'tab name {tab_name} is not file {self.excel_filename}')
        df = pd.read_excel(self.__excel_filename, sheet_name=tab_name)
        column_names = self.__get_column_names(df=df)
        return df.groupby(column_names[0])[column_names[2]].mean().reset_index()

    def _get_stdevs(self, tab_name: str= 'Sheet1') -> pd.DataFrame:
        """Return a dataframe containing standard deviations for each experiment in sheet."""
        if not self.__is_tab_name_in_file(tab_name=tab_name):
            raise ValueError(f'tab name {tab_name} is not file {self.excel_filename}')
        df = pd.read_excel(self.__excel_filename, sheet_name=tab_name)
        column_names = self.__get_column_names(df=df)
        return df.groupby(column_names[0])[column_names[3]].mean().reset_index()

    def get_num_observations(self, tab_name: str='Sheet1') -> np.ndarray:
        if not self.__is_tab_name_in_file(tab_name=tab_name):
            raise ValueError(f'tab name {tab_name} is not file {self.excel_filename}')
        df = pd.read_excel(self.__excel_filename, sheet_name=tab_name)
        column_names = self.__get_column_names(df=df)
        temp_df = df.groupby(column_names[0])[column_names[1]].count().reset_index()
        return temp_df[column_names[1]].to_numpy()
        # return np.array([100] * 3)   # that's all we need here, figure out how to get to the 3

    def get_average_of_averages(self, tab_name: str='Sheet1') -> Tuple[float, float]:
        averages: np.ndarray = self.__get_column_values(df=self._get_averages(tab_name=tab_name))
        stdevs: np.ndarray = self.__get_column_values(df=self._get_stdevs(tab_name=tab_name))
        num_observations: np.ndarray = self.get_num_observations(tab_name=tab_name)

        weighted_means = self.__get_weighted_mean(averages=averages, num_observations=num_observations)
        variance = np.sum(num_observations * (stdevs**2 + (averages - weighted_means)**2)) / np.sum(num_observations)
        std_dev_of_averages = (np.sqrt(variance))

        return weighted_means.item(), std_dev_of_averages.item()

    @staticmethod
    def __get_weighted_mean(averages: np.ndarray, num_observations: np.ndarray) -> np.ndarray:
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
