import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from argparse import ArgumentParser


# =========== METHODS ===========
def bubbleplot(
    filepath: str,
    output: str,
    delimiter: str = ",",
    x_column: str = None,
    y_column: str = None,
    title: str = None,
    x_label: str = None,
    y_label: str = None,
    size: str = None,
    hue: str = None,
    palette: str = None,
) -> None:
    """Generate a bubble plot from data in a CSV file and save the plot in multiple formats.

    Parameters:
        - filepath (str): The path to the input CSV file containing data for the bubble plot.
        - output (str): The path to save the output plot files (PDF, PNG, SVG).
        - delimiter (str, optional): The delimiter used in the CSV file. Default is ",".
        - x_column (str, optional): The column to be used for the x-axis. Default is None.
        - y_column (str, optional): The column to be used for the y-axis. Default is None.
        - title (str, optional): The title of the plot. Default is None.
        - x_label (str, optional): The label for the x-axis. Default is None.
        - y_label (str, optional): The label for the y-axis. Default is None.
        - size (str, optional): The column to be used for bubble size. Default is None.
        - hue (str, optional): The column to be used for grouping (coloring) the data. Default is None.
        - palette (str, optional): The color palette to use for different groups. Default is None.

    Returns:
        None

    Usage:
        - This function reads data from a CSV file and generates a bubble plot using seaborn.
        The resulting plot is saved in multiple formats (PDF, PNG, SVG).
    """
    sns.set_theme()

    # Control possible errors
    if x_column == "" or y_column == "":
        x_column = None
        y_column = None

    if hue == "":
        hue = None
    if palette == "":
        palette = None

    # Read CSV file
    data = pd.read_csv(filepath, sep=delimiter, header=0)

    # Plot
    fig = plt.figure(figsize=(10, 10))
    if title is not None and title != "":
        plt.title(title, fontsize=15, fontweight="bold", loc="center", pad=20)
    if x_label is not None and x_label != "":
        plt.xlabel(x_label)
    if y_label is not None and y_label != "":
        plt.ylabel(y_label)

    sns.scatterplot(
        data=data,
        x=x_column,
        y=y_column,
        size=size,
        palette=palette,
        hue=hue,
        alpha=0.7,
        sizes=(20, 1000),
        linewidth=0,
    )
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)

    output = f"{output}/bubbleplot"
    extensions = [".pdf", ".png", ".svg"]

    for ext in extensions:
        fig.savefig(f"{output}{ext}", bbox_inches="tight", dpi=300)


# =========== MAIN ===========
if __name__ == "__main__":
    parser = ArgumentParser(description="Generate a barplot from a CSV file.")
    parser.add_argument(
        "--filepath",
        type=str,
        help="File path of the CSV file",
        required=True,
        dest="filepath",
        metavar="STRING",
    )
    parser.add_argument(
        "--x-column",
        type=str,
        help="Column name for the x-axis of the plot",
        required=True,
        dest="x_column",
        metavar="STRING",
    )
    parser.add_argument(
        "--y-column",
        type=str,
        help="Column name for the y-axis of the plot",
        required=True,
        dest="y_column",
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
        "--x-label",
        type=str,
        help="Label of the x-axis",
        required=False,
        default=None,
        dest="x_label",
        metavar="STRING",
    )
    parser.add_argument(
        "--y-label",
        type=str,
        help="Label of the y-axis",
        required=False,
        default=None,
        dest="y_label",
        metavar="STRING",
    )
    parser.add_argument(
        "--size",
        type=str,
        help="Column for the size of the bubbles",
        default=None,
        required=False,
        dest="size",
    )
    parser.add_argument(
        "--hue",
        type=str,
        help="Column name for the hue of the plot",
        required=False,
        default=None,
        dest="hue",
        metavar="STRING",
    )
    parser.add_argument(
        "--palette",
        help="Palette of the boxplot if hue is present.",
        default=None,
        required=False,
        dest="palette",
        metavar="STRING",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        help="Delimiter of the CSV file",
        required=False,
        default=",",
        metavar="CHAR",
        dest="delimiter",
    )
    parser.add_argument(
        "--output-path",
        dest="output",
        default="/mnt/shared",
        help="Output path",
        required=False,
        metavar="STRING",
    )

    args = parser.parse_args()
    bubbleplot(
        filepath=args.filepath,
        delimiter=args.delimiter,
        x_column=args.x_column,
        y_column=args.y_column,
        title=args.title,
        x_label=args.x_label,
        y_label=args.y_label,
        size=args.size,
        hue=args.hue,
        palette=args.palette,
        output=args.output,
    )
