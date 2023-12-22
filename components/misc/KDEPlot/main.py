import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from argparse import ArgumentParser


# =========== METHODS ===========
def kdeplot(
    filepath: str,
    x_column: str,
    output_path: str,
    delimiter: str = ",",
    normalization: bool = True,
    palette: str = None,
    hue: str = None,
    title: str = None,
    x_label: str = None,
) -> None:
    """Generic KDE Plot
    Generate a KDE Plot from a csv file

    Args:
        filepath (str): Filepath of the csv file
        x_column (str): Column name for plot
        output_path (str): Output directory
        delimiter (str, optional): Delimiter of the csv file. Defaults to ",".
        normalization (bool, optional): Normalization of the data if true. Defaults to True.
        palette (str, optional): Palette Color. Defaults to None.
        hue (str, optional): Hue for plot. Defaults to None.
        title (str, optional): Title of the plot. Defaults to None.
        x_label (str, optional): Label of the x-axis. Defaults to None.

    Returns:
        None

    Usage:
        - This function reads data from a CSV file and generates a KDE Plot using seaborn.
        The resulting plot is saved in multiple formats (PDF, PNG, SVG).
    """
    sns.set_theme()
    # Read CSV file
    data = pd.read_csv(filepath, sep=delimiter)

    # Check if hue and palette are empty
    if hue == "":
        hue = None

    if palette == "":
        palette = None

    # Generate KDE Plot
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.kdeplot(
        data=data,
        x=x_column,
        hue=hue,
        fill=True,
        common_norm=normalization,
        palette=palette,
        alpha=0.5,
        linewidth=1,
        ax=ax,
        warn_singular=False,
    )
    if title and title != "":
        ax.set_title(title, fontsize=16, fontweight="bold", pad=20)
    if x_label and x_label != "":
        ax.set_xlabel(x_label)

    # Save plot
    file = f"{output_path}/kde_plot"
    extensions = [".pdf", ".png", ".svg"]

    for ext in extensions:
        fig.savefig(f"{file}{ext}", bbox_inches="tight", dpi=300)


# =========== MAIN ===========
if __name__ == "__main__":

    def as_bool(value: str) -> bool:
        if value.lower() in {"yes", "true", "t", "y", "1"}:
            return True
        elif value.lower() in {"no", "false", "f", "n", "0"}:
            return False
        else:
            raise ValueError(f"{value} is not a valid boolean value")

    parser = ArgumentParser(description="Generic KDE Plot")

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
        help="Column name for plot",
        dest="x_column",
        metavar="STRING",
    )
    parser.add_argument(
        "--normalization",
        type=as_bool,
        required=False,
        default="true",
        help="Normalization of the data if true",
        dest="normalization",
        metavar="BOOL",
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
        help="Palette Color",
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
        help="Label of the x-axis",
        dest="x_label",
        metavar="STRING",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        required=False,
        default=",",
        help="Delimiter of the csv file",
        dest="delimiter",
        metavar="CHAR",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        required=False,
        default="/mnt/shared",
        help="Output directory",
        dest="output",
        metavar="STRING",
    )

    args = parser.parse_args()

    kdeplot(
        filepath=args.filepath,
        x_column=args.x_column,
        normalization=args.normalization,
        palette=args.palette,
        hue=args.hue,
        title=args.title,
        x_label=args.x_label,
        delimiter=args.delimiter,
        output_path=args.output,
    )
