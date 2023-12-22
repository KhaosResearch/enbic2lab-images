import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from argparse import ArgumentParser

# =========== METHODS ===========
def regplot(
    filepath: str,
    x_column: str,
    y_column: str,
    output_path: str,
    color = None,
    title: str = None,
    x_label: str = None,
    y_label: str = None,
    delimiter: str = ",",
):
    """ Create a regression plot

    Args:
        - filepath (str): Filepath of the csv file
        - x_column (str): Column to plot in x axis
        - y_column (str): Column to plot in y axis
        - output_path (str): Output path
        - color (str): Color of the plot
        - title (str): Title of the plot
        - x_label (str): Label of the x axis
        - y_label (str): Label of the y axis
        - delimiter (str): Delimiter of the csv file
    
    Returns:
        - None
    """
    sns.set_theme()

    # Read data
    data = pd.read_csv(filepath, sep=delimiter)

    # Create plot
    fig = plt.figure(figsize=(10, 10))

    sns.regplot(
        data=data,
        x=x_column,
        y=y_column,
        color=color if color is not None else None,
    )
    plt.title(title, fontsize=20, fontweight="bold", pad=20) if title is not None else None
    plt.xlabel(x_label, fontsize=15) if x_label is not None else None
    plt.ylabel(y_label, fontsize=15) if y_label is not None else None

    # Save plot
    file = f"{output_path}/regplot"
    extensions = [".pdf", ".png", ".svg"]

    for ext in extensions:
        fig.savefig(f"{file}{ext}", bbox_inches="tight", dpi=300)


# =========== MAIN ===========
if __name__ == "__main__":
    parser = ArgumentParser(description="Regression Plot")
    parser.add_argument(
        "--filepath",
        type=str,
        help="Filepath of the csv file",
        required=True,
        dest="filepath",
        metavar="STRING",
    )
    parser.add_argument(
        "--x-column",
        type=str,
        help="Column to plot in x axis",
        required=True,
        dest="x_column",
        metavar="STRING",
    )
    parser.add_argument(
        "--y-column",
        type=str,
        help="Column to plot in y axis",
        required=True,
        dest="y_column",
        metavar="STRING",
    )
    parser.add_argument(
        "--color",
        type=str,
        help="Color of the plot",
        required=False,
        default="#5975a4",
        dest="color",
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
        help="Label of the x axis",
        required=False,
        default=None,
        dest="x_label",
        metavar="STRING",
    )
    parser.add_argument(
        "--y-label",
        type=str,
        help="Label of the y axis",
        required=False,
        default=None,
        dest="y_label",
        metavar="STRING",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        help="Delimiter of the csv file",
        required=False,
        default=",",
        dest="delimiter",
        metavar="CHAR",
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

    regplot(
        filepath=args.filepath,
        x_column=args.x_column,
        y_column=args.y_column,
        color=args.color,
        title=args.title,
        x_label=args.x_label,
        y_label=args.y_label,
        delimiter=args.delimiter,
        output_path=args.output,
    )