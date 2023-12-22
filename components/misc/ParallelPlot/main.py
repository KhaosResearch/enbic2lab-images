from typing import List

import matplotlib.pyplot as plt

import pandas as pd
from pandas.plotting import parallel_coordinates

from argparse import ArgumentParser


# =========== METHODS ===========
def parallel_plot(
    filepath: str,
    output_path: str,
    column: str,
    palette: str = None,
    title: str = None,
    delimiter: str = ",",
) -> None:
    """Parallel Plot

    Args:
        - filepath(str): Filepath of the csv file
        - output_path(str): Output path
        - column(str): Column to plot
        - palette(str): Color palette or list of colors
        - title(str): Title of the plot
        - delimiter(str): Delimiter of the csv file
    
    Returns:
        - None
    """
    plt.style.use("seaborn-v0_8-darkgrid")

    # Read data
    data = pd.read_csv(filepath, sep=delimiter)
    target = data.pop(column)

    # Drop non-numeric columns
    for col in data.columns:
        if data[col].dtype == "object":
            data.drop(col, axis=1, inplace=True)
    data = pd.concat([data, target], axis=1)

    values_to_plot = data[column].unique()

    # Get colors
    try:
        if palette is None:
            raise ValueError("No palette provided")
        cmap = plt.get_cmap(palette)
        color_list = [
            cmap(i / len(values_to_plot)) for i in range(1, len(values_to_plot) + 1)
        ]
    except ValueError as err:
        print(f"{err}.\nUsing default colors.")
        cmap = plt.get_cmap("viridis")
        color_list = [
            cmap(i / len(values_to_plot)) for i in range(1, len(values_to_plot) + 1)
        ]

    # Plot
    fig = plt.figure(figsize=(10, 10))
    parallel_coordinates(
        data,
        column,
        color=color_list,
        alpha=0.8,
        axvlines=True,
        axvlines_kwds={"color": "black", "alpha": 0.3, "linestyle": ":"},
    )
    plt.title(title, fontsize=16, fontweight="bold") if title is not None else None
    plt.xticks(rotation=90)
    plt.legend(loc="upper left", bbox_to_anchor=(1.01, 1), fontsize=12, frameon=True)

    # Save plot
    file = f"{output_path}/parallel_plot"
    extensions = [".pdf", ".png", ".svg"]

    for ext in extensions:
        fig.savefig(f"{file}{ext}", bbox_inches="tight", dpi=300)


# =========== METHODS ===========
if __name__ == "__main__":
    parser = ArgumentParser(description="Parallel Plot")
    parser.add_argument(
        "--filepath",
        type=str,
        help="Filepath of the csv file",
        required=True,
        dest="filepath",
        metavar="STRING",
    )
    parser.add_argument(
        "--column",
        type=str,
        help="Column to plot",
        required=True,
        dest="column",
        metavar="STRING",
    )
    parser.add_argument(
        "--palette",
        type=str,
        help="Color palette or list of colors",
        required=False,
        default=None,
        dest="palette",
        metavar="STRING",
    )
    parser.add_argument(
        "--title",
        type=str,
        help="Title of the plot",
        required=False,
        default=None,
        dest="title",
        metavar="STRING",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        help="Delimiter of the csv file",
        required=False,
        default=",",
        dest="delimiter",
        metavar="STRING",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        help="Output path",
        required=False,
        default="/mnt/shared",
        dest="output",
        metavar="STRING",
    )

    args = parser.parse_args()

    parallel_plot(
        filepath=args.filepath,
        column=args.column,
        palette=args.palette,
        title=args.title,
        delimiter=args.delimiter,
        output_path=args.output,
    )
