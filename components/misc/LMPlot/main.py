import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from argparse import ArgumentParser


# =========== METHODS ===========
def lmplot(
    filepath: str,
    x_column: str,
    y_column: str,
    output_path: str,
    hue: str = None,
    palette: str = None,
    title: str = None,
    x_label: str = None,
    y_label: str = None,
    delimiter: str = ",",
) -> None:
    """Generic LM Plot
    Generate a LM Plot from a csv file

    Args:
        - filepath (str): Filepath of the csv file
        - x_column (str): Column name for x axis
        - y_column (str): Column name for y axis
        - output_path (str): Output directory
        - hue (str, optional): Hue for plot. Defaults to None.
        - palette (str, optional): Color palette. Defaults to None.
        - title (str, optional): Title of the plot. Defaults to None.
        - x_label (str, optional): Label of the x-axis. Defaults to None.
        - y_label (str, optional): Label of the y-axis. Defaults to None.
        - delimiter (str, optional): Delimiter of the csv file. Defaults to ",".

    Returns:
        None

    Usage:
        - This function reads data from a CSV file and generates a LM Plot using seaborn.
        The resulting plot is saved in multiple formats (PDF, PNG, SVG).
    """
    sns.set_theme()

    # Check if hue and palette are empty
    if hue == "":
        hue = None
    if palette == "":
        palette = None

    # Read CSV file
    data = pd.read_csv(filepath, sep=delimiter)

    # Generate LM Plot
    lmp = sns.lmplot(
        data=data, x=x_column, y=y_column, hue=hue, palette=palette, height=7
    )

    if title and title != "":
        lmp.figure.suptitle(title, fontsize=15, fontweight="bold", y=1.05)
    if x_label and x_label != "":
        lmp.set(xlabel=x_label)
    if y_label and y_label != "":
        lmp.set(ylabel=y_label)

    # Save plot
    file = f"{output_path}/lmplot"
    extensions = [".pdf", ".png", ".svg"]

    for ext in extensions:
        lmp.savefig(f"{file}{ext}", bbox_inches="tight")


# =========== MAIN ===========
if __name__ == "__main__":
    parser = ArgumentParser(description="Generic LM Plot")

    parser.add_argument(
        "--filepath",
        type=str,
        required=True,
        help="Filepath of the csv file",
        dest="filepath",
        metavar="STRING",
    )
    parser.add_argument(
        "--x-column",
        type=str,
        required=True,
        help="Column name for x axis",
        dest="x_column",
        metavar="STRING",
    )
    parser.add_argument(
        "--y-column",
        type=str,
        required=True,
        help="Column name for y axis",
        dest="y_column",
        metavar="STRING",
    )
    parser.add_argument(
        "--hue",
        type=str,
        required=False,
        default=None,
        help="Hue for plot",
        dest="hue",
        metavar="STRING",
    )
    parser.add_argument(
        "--palette",
        type=str,
        required=False,
        default=None,
        help="Color palette for plot",
        dest="palette",
        metavar="STRING",
    )
    parser.add_argument(
        "--title",
        type=str,
        required=False,
        default=None,
        help="Title for plot",
        dest="title",
        metavar="STRING",
    )
    parser.add_argument(
        "--x-label",
        type=str,
        required=False,
        default=None,
        help="Label for x axis",
        dest="x_label",
        metavar="STRING",
    )
    parser.add_argument(
        "--y-label",
        type=str,
        required=False,
        default=None,
        help="Label for y axis",
        dest="y_label",
        metavar="STRING",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        required=False,
        default=",",
        help="Delimiter of the csv file",
        dest="delimiter",
        metavar="STRING",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        required=False,
        default="/mnt/shared",
        help="Output path for plot",
        dest="output",
        metavar="STRING",
    )

    args = parser.parse_args()

    lmplot(
        filepath=args.filepath,
        x_column=args.x_column,
        y_column=args.y_column,
        hue=args.hue,
        palette=args.palette,
        title=args.title,
        x_label=args.x_label,
        y_label=args.y_label,
        delimiter=args.delimiter,
        output_path=args.output,
    )
