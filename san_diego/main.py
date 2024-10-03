#!/usr/bin/env python3
import os
import numpy as np
from matplotlib import pyplot as plt
from src.utility import _Utility
from src.spreadsheet import Spreadsheet
from src.weighted_average import WeightedAverage
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


def main():
    data_dir = _Utility.get_user_data_dir_path()
    project_dir = "chips_for_san_diego"
    plot_dir = os.path.join(data_dir, project_dir)

    _Utility.matplotlib_render_latex()

    excel_filenames = os.listdir(os.path.join(data_dir, project_dir))
    excel_filenames = list(filter(lambda x: x if "xlsx" in x else "", excel_filenames))

    x_label = "injection ID"
    y_label = r"R ($K\Omega$)"
    x_ticks = np.array(list(range(1, 4)))

    for excel_filename in excel_filenames:
        logger.info("Processing {}".format(excel_filename))
        # if excel_filename != 'resistance_series_F.xlsx':
        #     continue
        excel_filename = os.path.join(data_dir, project_dir, excel_filename)
        spreadsheet = Spreadsheet(excel_filename=excel_filename)

        weighted_averages: list[dict] = []

        # Create a list of dictionaries, where each dictionary has three items: the injection ID,
        # the average resistance associated with the injection ID, and the associated
        # standard deviation.
        for sheet_name in spreadsheet.sheet_names:
            print(f"\nsheet_name: {sheet_name}:")
            df = spreadsheet.get_dataframe(tab_name=sheet_name)
            weighted_average = WeightedAverage(
                df=df, num_obs=spreadsheet.NUMBER_OF_SAMPLES
            )
            # print(weighted_average.get_weighted_average())
            data = weighted_average.get_weighted_average().to_dict(orient="list")
            _write_to_csv_file(
                csv_filename=os.path.join(
                    plot_dir,
                    f"{_Utility.get_filename_only(excel_filename, is_filename_only=True)}.csv",
                ),
                chipID=sheet_name,
                data=[
                    {key: val[0] if len(val) > 0 else None for key, val in data.items()}
                ],
            )
            weighted_averages.append(
                data
            )  # weighted_average.get_weighted_average().to_dict(orient='list'))

        # Create a figure and subplots.
        array_dimension: int = len(weighted_averages)
        if array_dimension == 1:
            # The spreadsheet only contains one tab. That makes axs only one dimensional not
            # indexable. In that case we need to set squeeze to `False` to ensure we get a 2D array,
            # which can be indexed. Otherwise, we get in index error.
            fig, axs = plt.subplots(
                array_dimension,
                1,
                squeeze=False,
                figsize=(8, len(weighted_averages) * 4),
            )
            axs = axs.flatten()
        else:
            fig, axs = plt.subplots(
                array_dimension,
                1,
                squeeze=True,
                figsize=(8, len(weighted_averages) * 4),
            )
        # for avg in weighted_averages:
        #     print(avg)

        # Iterate over data sets and plot each one in its own subplot.
        for i, data in enumerate(weighted_averages):
            labels: list = list(data.keys())
            axs[i].errorbar(
                data[labels[0]],
                data[labels[1]],
                yerr=data[labels[2]],
                fmt="-o",
                label=spreadsheet.sheet_names[i],
            )
            axs[i].set_xlabel(x_label)
            axs[i].set_ylabel(y_label)
            axs[i].legend()
            axs[i].set_xticks(x_ticks)

        # Adjust layout.
        plt.tight_layout()

        # Show the plot.
        # plt.show()

        figure_name = _Utility.get_filename_only(excel_filename)
        plt.savefig(os.path.join(plot_dir, figure_name), bbox_inches="tight")


def _write_to_csv_file(csv_filename: str, chipID: str, data: list[dict]) -> None:
    csv_filename = f"{_Utility.get_filename_only(csv_filename)}.csv"
    logger.info(f"Writing data to {csv_filename}")
    data[0]["chipID"] = chipID
    _Utility.write_row_to_csv_file(csv_filename=csv_filename, data=data)


if __name__ == "__main__":
    main()
