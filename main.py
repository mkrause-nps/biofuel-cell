#!/usr/bin/env python3

import pandas as pd
from src.clearanceprotocol import ClearanceProtocol
from src.ingest import Ingest
from src.utility import _Utility
from src.plotter import Plotter


def main():

    df: pd.DataFrame = Ingest.read_data_from_excel(filename=None)
    df.columns = _Utility.remove_whitespace_from_pd_header(df.columns)
    df.columns = _Utility.remove_undesired_symbols_from_pd_header(df.columns)
    # print(df.head())

    clearance_protocols = []
    for i in range(1, Ingest.get_number_of_groups() + 1):
        group_name: str = f"group{i}"
        chip_id_lst: list = Ingest.get_chip_id_for_clearance_group(group_name)
        clearance_values: df = Ingest.get_clearance_values_for_group(
            df=df, group_chip_ids=chip_id_lst
        )
        clearance_protocol = ClearanceProtocol(
            protocol_id=i,
            name=group_name,
            chip_id_lst=chip_id_lst,
            percent_cleared=clearance_values,
        )
        clearance_protocols.append(clearance_protocol)

    for prot in clearance_protocols:
        grouped: pd.DataFrame.GroupedBy = Ingest.get_df_grouped_by_chip_section(
            prot.percent_cleared
        )
        data = Plotter.create_data_structure_for_plotting(
            grouped=grouped, y_column_name="percent_cleared"
        )
        Plotter.simple_plot(data=data, group_name=prot.name)
        Plotter.save_figure(
            data_path_dir=_Utility.get_user_data_dir_path(), fig_name=prot.name
        )


if __name__ == "__main__":
    main()
