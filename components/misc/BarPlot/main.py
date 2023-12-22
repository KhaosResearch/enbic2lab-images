import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from argparse import ArgumentParser


# =========== METHODS ===========
def barplot(
    filepath: str,
    output: str,
    delimiter: str = ",",
    x_column: str = None,
    y_column: str = None,
    title: str = None,
    x_label: str = None,
    y_label: str = None,
    orient: str = "vertical",
    color: str = "#5975a4",
) -> None:
    """Generate a bar plot from data in a CSV file and save the plot in multiple formats.

    Parameters:
        - filepath (str): The path to the input CSV file containing data for the bar plot.
        - output (str): The path to save the output plot files (PDF, PNG, SVG).
        - delimiter (str, optional): The delimiter used in the CSV file. Default is ",".
        - x_column (str, optional): The column to be used for the x-axis. Default is None.
        - y_column (str, optional): The column to be used for the y-axis. Default is None.
        - title (str, optional): The title of the plot. Default is None.
        - x_label (str, optional): The label for the x-axis. Default is None.
        - y_label (str, optional): The label for the y-axis. Default is None.
        - orient (str, optional): The orientation of the plot ('vertical' or 'horizontal').
        Default is 'vertical'.
        - color (str, optional): The color of the bars. Default is '#5975a4'.

    Returns:
        None

    Usage:
        - This function reads data from a CSV file and generates a bar plot using seaborn.
        The resulting plot is saved in multiple formats (PDF, PNG, SVG).
    """
    sns.set_theme()
    # Control possible errors
    match orient:
        case "vertical":
            orient = "v"
        case "horizontal":
            orient = "h"
        case _ as invalid:
            raise ValueError(
                f"Invalid orientation({invalid}). Use 'vertical' or 'horizontal'."
            )

    if color == "":
        color = None

    if x_column == "" or y_column == "":
        x_column = None
        y_column = None

    # Read CSV file
    data = pd.read_csv(filepath, sep=delimiter)

    # Plot
    fig = plt.figure(figsize=(10, 10))
    if title is not None and title != "":
        plt.title(title, fontsize=15, fontweight="bold", loc="center", pad=20)
    if x_label is not None and x_label != "":
        plt.xlabel(x_label)
    if y_label is not None and y_label != "":
        plt.ylabel(y_label)

    sns.barplot(
        data=data,
        x=x_column,
        y=y_column,
        orient=orient,
        color=color,
        native_scale=True,
        capsize=0.2,
    )

    output = f"{output}/barplot"
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
        "--orient",
        type=str.lower,
        help="Orientation of the plot, 'vertical' or 'horizontal'",
        choices=["vertical", "horizontal"],
        default="vertical",
        required=False,
        dest="orient",
    )
    parser.add_argument(
        "--color",
        help="Color of the barplots.",
        default="#5975a4",
        required=False,
        dest="color",
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
    barplot(
        filepath=args.filepath,
        delimiter=args.delimiter,
        x_column=args.x_column,
        y_column=args.y_column,
        title=args.title,
        x_label=args.x_label,
        y_label=args.y_label,
        orient=args.orient,
        color=args.color,
        output=args.output,
    )
