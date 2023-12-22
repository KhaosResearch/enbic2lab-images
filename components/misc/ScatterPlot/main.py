import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from argparse import ArgumentParser
from random import randint


# ====== METHODS =====
def scatterplot(
    filepath: str,
    output_path: str,
    x_column: str,
    y_column: str,
    hue: str = None,
    palette: str = "tab10",
    title: str = None,
    x_label: str = None,
    y_label: str = None,
    delimiter: str = ",",
):
    """Scatter plot
    This function generates a scatter plot from a CSV file.
    
    Args:
        - filepath (str): File path of the CSV file
        - output_path (str): Path to save the plot
        - x_column (str): Column name for the x axis of the plot
        - y_column (str): Column name for the y axis of the plot
        - hue (str, optional): Column name for hue. Defaults to None.
        - palette (str, optional): Color palette of the plot. If hue is not specified, the first color of the palette will be used. Defaults to "tab10".
        - title (str, optional): Title of the plot. Defaults to None.
        - x_label (str, optional): Label of the x axis. Defaults to None.
        - y_label (str, optional): Label of the y axis. Defaults to None.
        - delimiter (str, optional): Delimiter of the CSV file. Defaults to ",".
    
    Returns:
        - None
    
    Raises:
        - ValueError: Invalid hue
        - ValueError: Invalid palette
    """
    sns.set_theme()

    # Load data
    data = pd.read_csv(filepath, delimiter=delimiter)

    # Check if hue is empty
    if hue == "":
        hue = None

    # Plot
    fig = plt.figure(figsize=(10, 10))

    sns.scatterplot(
        data=data,
        x=x_column,
        y=y_column,
        hue=hue,
        palette=palette if hue else None,
        color=None if hue else sns.color_palette(palette, 10)[randint(0, 9)],
        linewidth=0,
        s=50,
    )
    plt.grid(True)

    if hue:
        plt.legend(loc="upper left", bbox_to_anchor=(1.01, 1), fontsize=12)

    plt.title(title, fontsize=16, pad=20, fontweight="bold") if title else None
    plt.xlabel(x_label, fontsize=12, labelpad=10) if x_label else None
    plt.ylabel(y_label, fontsize=12, labelpad=10) if y_label else None

    # Save the plot
    file = f"{output_path}/scatterplot"
    extensions = [".pdf", ".png", ".svg"]

    for ext in extensions:
        fig.savefig(f"{file}{ext}", bbox_inches="tight", dpi=300)


# ===== MAIN =====
if __name__ == "__main__":
    parser = ArgumentParser(description="Scatter plot")
    parser.add_argument(
        "--filepath",
        type=str,
        required=True,
        help="File path of the CSV file",
        dest="filepath",
        metavar="STRING",
    )
    parser.add_argument(
        "--x-column",
        type=str,
        required=True,
        help="Column name for the x axis of the plot",
        dest="x_column",
        metavar="STRING",
    )
    parser.add_argument(
        "--y-column",
        type=str,
        required=True,
        help="Column name for the y axis of the plot",
        dest="y_column",
        metavar="STRING",
    )
    parser.add_argument(
        "--hue",
        type=str,
        required=False,
        default=None,
        help="Column name for hue.",
        dest="hue",
        metavar="STRING",
    )
    parser.add_argument(
        "--palette",
        type=str,
        required=False,
        default="tab10",
        help="Color palette of the plot. If hue is not specified, the first color of the palette will be used.",
        dest="palette",
        metavar="STRING",
    )
    parser.add_argument(
        "--title",
        type=str,
        required=False,
        default=None,
        help="Title of the plot",
        dest="title",
        metavar="STRING",
    )
    parser.add_argument(
        "--x-label",
        type=str,
        required=False,
        default=None,
        help="Label of the x axis",
        dest="x_label",
        metavar="STRING",
    )
    parser.add_argument(
        "--y-label",
        type=str,
        required=False,
        default=None,
        help="Label of the y axis",
        dest="y_label",
        metavar="STRING",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        required=False,
        default=",",
        help="Delimiter of the CSV file",
        dest="delimiter",
        metavar="STRING",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        required=False,
        default="/mnt/shared",
        help="Path to save the plot",
        dest="output",
        metavar="STRING",
    )

    args = parser.parse_args()

    scatterplot(
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
