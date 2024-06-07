#!/usr/bin/env python3

import os
import configparser
import pandas as pd


class Ingest(object):
    """Utility class to ingest data into a dataframe."""

    script_dir = os.path.dirname(os.path.abspath(__file__))
    home = os.path.expanduser("~")
    config_file = os.path.join(script_dir, "..", "config.ini")
    config = configparser.ConfigParser()

    @classmethod
    def get_excel_filename(cls) -> str:
        """Returns absolute path to Excel file."""
        cls.config.read(cls.config_file)

        return os.path.join(
            cls.home,
            cls.config["Constants"]["data_path"],
            cls.config["Constants"]["excel_file"],
        )

    @classmethod
    def read_data_from_excel(cls, filename: str) -> pd.DataFrame:
        sheet_name = cls.config["Constants"]["sheet_name"]
        return pd.read_excel(filename, sheet_name=sheet_name)

    @classmethod
    def get_number_of_groups(cls) -> int:
        return int(cls.config["Constants"]["num_groups"])

    # @staticmethod
    # def get_groups(id_s: List[int]) -> List[ClearanceProtocol]:
    #     return [ClearanceProtocol(id=id_, name=f'group{id_}', value=[]) for id_ in id_s]

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
        """Returns a grouped_by object grouped by the chip's section."""
        return df.groupby(cls.config["Constants"]["chip_section"])
