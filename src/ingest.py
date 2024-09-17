#!/usr/bin/env python3

import os
from typing import Union
import pandas as pd
from src.utility import _Utility


class Ingest(object):
    """Provides methods to ingest data into a dataframe."""

    # Class variables:
    config = _Utility.get_config()
    HOME = _Utility.home

    @classmethod
    def get_excel_filename(cls) -> str:
        """Returns absolute path to Excel file."""
        return cls.config["Constants"]["excel_file"]

    @classmethod
    def get_sheet_names(cls, filename: str) -> tuple:
        excel_file = pd.ExcelFile(filename)
        return tuple(excel_file.sheet_names)

    @classmethod
    def read_data_from_excel(
        cls, filename: Union[str | None], sheet_name: Union[str | None] = None
    ) -> pd.DataFrame:
        """Reads data from a specific sheet in Excel file."""
        if not sheet_name:
            sheet_name = cls.config["Constants"]["sheet_name"]
        if filename is None:
            filename = cls.get_excel_filename()
        filename = os.path.join(_Utility.get_user_data_dir_path(), filename)
        return pd.read_excel(filename, sheet_name=sheet_name)

    @classmethod
    def get_number_of_groups(cls) -> int:
        return int(cls.config["Constants"]["num_groups"])

    @classmethod
    def get_chip_id_for_clearance_group(cls, group_name: str) -> list:
        """Returns list of chip IDs."""
        lst_ = cls.config.get("ChipIDs", group_name)
        # Need to remove commas here, which are left-overs from the *.ini file.
        return [int(item.strip()) for item in lst_.split(",")]

    @classmethod
    def get_clearance_values_for_group(
        cls, df: pd.DataFrame, group_chip_ids: list
    ) -> pd.DataFrame:
        return df[df[cls.config["Constants"]["chip_id"]].isin(group_chip_ids)]

    @classmethod
    def get_df_grouped_by_chip_section(cls, df: pd.DataFrame) -> pd.DataFrame.groupby:
        """Returns a grouped_by object grouped by the chips' sections."""
        return df.groupby(cls.config["Constants"]["chip_section"])
