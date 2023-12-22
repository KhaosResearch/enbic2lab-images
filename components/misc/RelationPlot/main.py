import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from argparse import ArgumentParser

# =========== METHODS ===========
def relplot(
    filepath: str,
    x_column: str,
    y_column: str,
    output_path: str,
    hue: str =  None,
    kind: str = "scatter",
    style: str = None,
    col: str = None,
    row: str = None,
    palette: str = "tab10",
    size: str = None,
    delimiter: str = ",",
):
    """Plot a relational plot

    Args:
        - filepath (str): Filepath of the csv file
        - x_column (str): Column name of the x axis
        - y_column (str): Column name of the y axis
        - output_path (str): Path to save the plot
        - hue (str, optional): Column name for hue. Defaults to None.
        - kind (str, optional): Kind of the plot. Possible values are: scatter, line. Defaults to "scatter".
        - style (str, optional): Column name to classify by style. Defaults to None.
        - col (str, optional): Column name to divide the plot by columns. Defaults to None.
        - row (str, optional): Column name to divide the plot by rows. Defaults to None.
        - palette (str, optional): Color palette for plot. Defaults to "tab10".
        - size (str, optional): Column name to classify the plot by size. Defaults to None.
        - title (str, optional): Title of the plot. Defaults to None.
        - delimiter (str, optional): Delimiter of the csv file. Defaults to ",".
    
    Returns:
        - None
    """
    sns.set_theme()

    # Check if the file exists
    data = pd.read_csv(filepath, sep=delimiter)

    # Plot the data
    rp = sns.relplot(
        data=data,
        x=x_column,
        y=y_column,
        kind=kind if kind.lower() in ["scatter", "line"] else "scatter",
        height=7,   # When data is too large and the col and row are not None, the plot may be too small
        hue=hue if hue is not None or hue == "" else None,
        col=col if col is not None or col == "" else None,
        row=row if row is not None or row == "" else None,
        sizes=(10, 100),
        size=size if size is not None or size == "" else None,
        style=style if style is not None or style == "" else None,
        palette=palette if palette is not None or palette == "" else "tab10",
        linewidth=0 if kind.lower() == "scatter" else 1,
        alpha=0.8,
    )

    file = f"{output_path}/relplot"
    extensions = [".pdf", ".png", ".svg"]

    for ext in extensions:
        rp.savefig(f"{file}{ext}", bbox_inches="tight", dpi=500)


# =========== MAIN ===========
if __name__ == "__main__":
    parser = ArgumentParser(description="Relational Plot")
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
        help="Column name of the x axis",
        required=True,
        dest="x_column",
        metavar="STRING",
    )
    parser.add_argument(
        "--y-column",
        type=str,
        help="Column name of the y axis",
        required=True,
        dest="y_column",
        metavar="STRING",
    )
    parser.add_argument(
        "--palette",
        type=str,
        help="Color palette for plot",
        required=False,
        default="tab10",
        dest="palette",
        metavar="STRING",
    )
    parser.add_argument(
        "--hue",
        type=str,
        help="Column name for hue",
        required=False,
        default=None,
        dest="hue",
        metavar="STRING",
    )
    parser.add_argument(
        "--kind",
        type=str.lower,
        help="Kind of the plot. Possible values are: scatter, line",
        required=False,
        default="scatter",
        choices=["scatter", "line"],
        dest="kind",
        metavar="STRING",
    )
    parser.add_argument(
        "--style",
        type=str,
        help="Column name to classify by style",
        required=False,
        default=None,
        dest="style",
        metavar="STRING",
    )
    parser.add_argument(
        "--col",
        type=str,
        help="Column name to divide the plot by columns",
        required=False,
        default=None,
        dest="col",
        metavar="STRING",
    )
    parser.add_argument(
        "--row",
        type=str,
        help="Column name to divide the plot by rows",
        required=False,
        default=None,
        dest="row",
        metavar="STRING",
    )
    parser.add_argument(
        "--size",
        type=str,
        help="Column name to classify the plot by size",
        required=False,
        default=None,
        dest="size",
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
        help="Path to save the plot",
        required=False,
        default="/mnt/shared",
        dest="output",
        metavar="STRING",
    )

    args = parser.parse_args()

    relplot(
        filepath=args.filepath,
        x_column=args.x_column,
        y_column=args.y_column,
        hue=args.hue,
        kind=args.kind,
        style=args.style,
        col=args.col,
        row=args.row,
        palette=args.palette,
        size=args.size,
        delimiter=args.delimiter,
        output_path=args.output,
    )