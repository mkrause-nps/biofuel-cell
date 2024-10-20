#!/usr/bin/env python3
import configparser
import os
import csv
from pathlib import Path
import pandas as pd
from matplotlib import pyplot as plt


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

    @staticmethod
    def matplotlib_render_latex() -> None:
        plt.rcParams["text.usetex"] = True

    @staticmethod
    def remove_outliers(group: pd.Series, dataset_name: str) -> pd.Series:
        """If a number is not between the first and third quartiles, remove the outlier."""
        q1: float = group.quantile(0.25)
        q3: float = group.quantile(0.75)
        iqr: float = q3 - q1
        # Outlier criterion
        outliers: pd.Series[bool] = (group < (q1 - 1.5 * iqr)) | (
            group > (q3 + 1.5 * iqr)
        )
        if any(outliers):
            print(f"Found {outliers.sum()} outliers in {dataset_name} {group.name}!")
        return group[~outliers]

    @staticmethod
    def get_filename_only(filename: str, is_filename_only: bool = False) -> str:
        """Return absolute path of filename without extension, unless is_filename_only is set."""
        filename_path = filename.split(".")[0]
        if is_filename_only:
            return filename_path.split("/")[-1]
        return filename_path

    @staticmethod
    def put_value_in_row(
        row: pd.Series,
        condition_column_name: str,
        condition: str,
        value: int,
        alt_value: int,
    ) -> int:
        """Return one of two integers, depending on a value in same record but different column."""
        if row[condition_column_name] != condition:
            return alt_value
        return value

    @staticmethod
    def write_row_to_csv_file(csv_filename: str, data: list[dict]):
        """Write one record per line to a CSV file."""
        if len(data) == 0:
            msg = f"data is empty."
            raise IndexError(msg)
        fieldnames = list(dict(sorted(data[0].items())))  # list(data[0].keys())  # sort by keys
        with open(csv_filename, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header only if the file is empty.
            if csvfile.tell() == 0:
                writer.writeheader()

            # Write the data rows.
            for row in data:
                writer.writerow(row)

    @staticmethod
    def is_absolute_path(path: str) -> bool:
        return Path(path).is_absolute()

    @staticmethod
    def path_exists(path: Path) -> bool:
        """Check if a path exists."""
        if path.exists():
            return True
        return False

    @staticmethod
    def dir_exists(path: Path) -> bool:
        """Check if a directory exists."""
        if path.is_dir():
            return True
        return False

    @staticmethod
    def file_exists(path: Path) -> bool:
        """Check if a file exists."""
        if path.is_file():
            return True
        return False
