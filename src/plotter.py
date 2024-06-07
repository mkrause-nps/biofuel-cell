#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt


class Plotter(object):

    @staticmethod
    def simple_plot(data: dict) -> None:
        fig, ax = plt.subplots()
        for key, val in data.items():
            x = val["x"]
            y = val["y"]
            ax.scatter(x, y, label=key)

        # ax.set_title(data[])
        ax.set_xlabel("Chip Section")
        ax.set_ylabel("% cleared")

        # Customize the x-axis
        ax.set_xlim(0, 3)  # Set the limits of the x-axis from 0 to 3
        ax.set_xticks([1, 2])  # Set the x-axis to show only ticks at 1 and 2
        # Customize the y-axis
        ax.set_ylim(0, 100)  # Set the limits of the x-axis from 0 to 3

        plt.show()

    @staticmethod
    def create_data_structure_for_plotting(
        grouped: pd.DataFrame.groupby, y_column_name: str
    ) -> dict:
        data: dict[str, dict] = {}
        for x_column_name, group in grouped:
            data[x_column_name] = {
                "x": [x_column_name] * 3,
                "y": group[y_column_name].to_list(),
            }

        return data
