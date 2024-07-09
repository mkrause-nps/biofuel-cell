#!/usr/bin/env python3
import configparser
import os
import pandas as pd


class _Utility(object):
    """Private class of helper methods."""

    script_dir = os.path.dirname(os.path.abspath(__file__))
    home = os.path.expanduser("~")
    config_file = os.path.join(script_dir, "..", "config.ini")

    @classmethod
    def get_config(cls) -> configparser.ConfigParser:
        return configparser.ConfigParser()

    @classmethod
    def get_user_data_dir_path(cls) -> str:
        config = cls.get_config()
        config.read(cls.config_file)
        return os.path.join(cls.home, config["Constants"]["data_path"])

    @staticmethod
    def remove_whitespace_from_pd_header(columns: pd.DataFrame.columns) -> pd.DataFrame:
        return columns.str.replace(" ", "")

    @staticmethod
    def remove_undesired_symbols_from_pd_header(
        columns: pd.DataFrame.columns,
    ) -> pd.DataFrame:
        return columns.str.replace("%", "percent_")
