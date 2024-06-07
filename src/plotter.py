#!/usr/bin/env python3
import os
import re

import pandas as pd
import matplotlib.pyplot as plt


class Plotter(object):

    fig: plt.Figure = None

    @classmethod
    def simple_plot(cls, data: dict, group_name: str=None) -> None:
        cls.fig, ax = plt.subplots(figsize=(3, 6))
        for key, val in data.items():
            x = val["x"]
            y = val["y"]
            ax.scatter(x, y, label=key, s=25)

        if group_name:
            group_name = group_name.replace("group", "protocol")
            group_name = re.sub(r'(\D)(\d)', r'\1 \2', group_name)
            group_name = group_name.capitalize()
            ax.set_title(group_name)
        ax.set_xlabel("chip section")
        ax.set_ylabel("% cleared")

        # Add dashed line for easier data interpretation.
        y_value = 100  # The y-value where you want the horizontal line
        ax.axhline(y=y_value, color='r', linestyle='--')  # Add dashed horizontal line at y_value

        # Customize the x-axis
        ax.set_xlim(0, 3)
        ax.set_xticks([1, 2])  # Set the x-axis to show only ticks at 1 and 2
        # Customize the y-axis
        ax.set_ylim(0, 120)

        cls.fig.tight_layout()  # Adjust layout to prevent labels from being cut off.

        #plt.show()

    @staticmethod
    def create_data_structure_for_plotting(
        grouped: pd.DataFrame.groupby, y_column_name: str
    ) -> dict:
        """Returns a data structure that makes it convenient for plotting."""
        data: dict[str, dict] = {}
        for x_column_name, group in grouped:
            data[x_column_name] = {
                "x": [x_column_name] * 3,
                "y": group[y_column_name].to_list(),
            }

        return data

    @classmethod
    def save_figure(cls, data_path_dir: str, fig_name: str=None, fig_format: str='png') -> None:
        fig_name = f'{fig_name}.{fig_format}'
        fig_path = os.path.join(data_path_dir, fig_name)
        print(f'Saving figure to {fig_path}')
        cls.fig.savefig(fig_path, format=fig_format)
