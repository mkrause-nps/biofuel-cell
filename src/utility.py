#!/usr/bin/env python3
import configparser
import os
import pandas as pd


class _Utility(object):
    """Private class of helper methods."""

    script_dir = os.path.dirname(os.path.abspath(__file__))
    home = os.path.expanduser("~")
    config_file = os.path.join(script_dir, "..", "config.ini")
    config = configparser.ConfigParser()

    @classmethod
    def read_config(cls) -> configparser.ConfigParser:
        cls.config.read(cls.config_file)
        return cls.config

    @classmethod
    def get_user_data_dir_path(cls) -> str:
        return os.path.join(cls.home, cls.config["Constants"]["data_path"])

    @staticmethod
    def remove_whitespace_from_pd_header(columns: pd.DataFrame.columns) -> pd.DataFrame:
        return columns.str.replace(" ", "")

    @staticmethod
    def remove_undesired_symbols_from_pd_header(
        columns: pd.DataFrame.columns,
    ) -> pd.DataFrame:
        return columns.str.replace("%", "percent_")
