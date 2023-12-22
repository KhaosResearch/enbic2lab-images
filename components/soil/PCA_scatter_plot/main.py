from typing import List
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from argparse import ArgumentParser
from sklearn.preprocessing import LabelEncoder


def pca_scatter_plot(
    filepath: str,
    delimiter: str,
    x_axis: str,
    y_axis: str,
    output: str,
    color_list: List[str],
    target_column: str = None,
):
    """Generate a scatter plot from the resulted data of a PCA.

    This function reads data from a CSV file, performs PCA, and creates a scatter plot using two specified columns as the X and Y axes. The plot is saved in PDF format.

    Args:
        - filepath (str): The path to the CSV file containing the data for PCA and scatter plot.
        - delimiter (str): Delimiter used in the CSV file to separate values (e.g., ',' or ';').
        - x_axis (str): The column name to use as the X-axis in the scatter plot.
        - y_axis (str): The column name to use as the Y-axis in the scatter plot.
        - output (str): The path to save the PCA scatter plot in PDF format.
        - color_list (List[str]): List of colors to use in the scatter plot. One color per target label.
        - target_column (str): The column name to use as the target column. If not specified, the scatter plot will be generated without target labels.

    Raises:
        - FileNotFoundError: If the PCA scatter plot could not be saved.

    Example:
        To create a PCA scatter plot from data in a CSV file 'data.csv' with ';' as the delimiter, using the 'X' column as the X-axis and the 'Y' column as the Y-axis, and save it as 'scatter_plot.pdf':

        >>> pca_scatter_plot(filepath="data.csv", delimiter=";", x_axis="X", y_axis="Y", output="scatter_plot.pdf")

    Note:
        - The function performs PCA to reduce the dimensionality of the data before creating the scatter plot.
        - The scatter plot is saved in PDF format.
    """

    df = pd.read_csv(filepath, sep=delimiter, decimal=".", header=0)

    if target_column != None:
        target_names = np.unique(df[target_column])
        y = df[[target_column]]
        df = df.drop([target_column], axis=1)
    else:
        target_names = ["unique_class"]
        y = pd.Series(target_names * len(df.index))

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y.values.ravel())

    if len(color_list) != len(target_names):
        raise ValueError(
            f"There should be the same number of colors as labels.\nNumber of different labels: {len(target_names)} | Number of colors provided:{len(color_list)}"
        )

    pc_labels = list(df.columns.values)
    if (x_axis not in pc_labels) or (y_axis not in pc_labels):
        raise ValueError(f"The PC columns avaliable are: {pc_labels}")

    fig = plt.figure()

    for color_list, i, target_name in zip(
        color_list, np.arange(0, len(target_names)), target_names
    ):
        plt.scatter(
            df.loc[y == i, x_axis],
            df.loc[y == i, y_axis],
            color=color_list,
            alpha=0.8,
            lw=1,
            label=target_name,
        )
    if target_column != "":
        plt.legend(loc="best", shadow=False, scatterpoints=1)

    plt.title("PCA")
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)

    fig.savefig(output, bbox_inches="tight")


if __name__ == "__main__":
    parser = ArgumentParser(description="Write the PCA scatter plot into a PDF file")
    parser.add_argument(
        "--filepath",
        type=str,
        help="Path to the CSV file",
        required=True,
        metavar="STRING",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        help="Delimiter of the CSV file",
        required=False,
        default=";",
        metavar="CHAR",
    )
    parser.add_argument(
        "--x-axis",
        dest="x_axis",
        type=str,
        help="Name of the X axis",
        required=True,
        metavar="STRING",
    )
    parser.add_argument(
        "--y-axis",
        dest="y_axis",
        type=str,
        help="Name of the Y axis",
        required=True,
        metavar="STRING",
    )
    parser.add_argument(
        "--color-list",
        dest="color_list",
        type=str,
        help="List of colors to use in the scatter plot. One color per target label. List separated by ',' (e.g., 'red,blue, green')",
        required=True,
        metavar="STRING",
    )
    parser.add_argument(
        "--target-column",
        dest="target_column",
        type=str,
        help="Name of the target column",
        required=False,
        metavar="STRING",
        default=None,
    )
    parser.add_argument(
        "--output-path",
        dest="output",
        type=str,
        help="Path to save the PCA scatter plot in PDF format",
        required=False,
        default="/mnt/shared",
        metavar="STRING",
    )

    args = parser.parse_args()

    args.color_list = args.color_list.replace(" ", "").split(",")

    pca_scatter_plot(
        filepath=args.filepath,
        delimiter=args.delimiter,
        x_axis=args.x_axis,
        y_axis=args.y_axis,
        color_list=args.color_list,
        target_column=args.target_column,
        output=args.output+"/PCA_plot.pdf",
    )
