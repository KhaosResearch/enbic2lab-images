import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from argparse import ArgumentParser


# ========= METHODS =========
def line_chart(
    filepath: str,
    x_column: str,
    y_column: str,
    output_path: str,
    hue: str = None,
    palette: str = None,
    style: str = None,
    markers: bool = False,
    dashes: bool = False,
    grid: bool = True,
    ci: bool = True,
    legend: bool = True,
    title: str = None,
    x_label: str = None,
    y_label: str = None,
    delimiter: str = ",",
) -> None:
    """# Line chart plot

    This function reads data from a CSV file and generates a line chart using seaborn. The resulting plot is saved in multiple formats (PDF, PNG, SVG).

    Args:
        - filepath (str): File path of the CSV file
        - x_column (str): Column name for the x axis of the plot
        - y_column (str): Column name for the y axis of the plot
        - output_path (str): Output path of the plot
        - hue (str, optional): Column name for hue. Defaults to None.
        - palette (str, optional): Palette of colors for the plot. Defaults to None.
        - style (str, optional): Column name for styles of the lines. Defaults to None.
        - markers (bool, optional): Show different markers. Must be with style param. Defaults to False.
        - dashes (bool, optional): Show different lines. Must be with style param. Defaults to False.
        - grid (bool, optional): Show grid. Defaults to True.
        - ci (bool, optional): Show confidence interval of 95%. None for quit interval. Defaults to True.
        - legend (bool, optional): Show legend. Defaults to True.
        - title (str, optional): Title of the plot. Defaults to None.
        - x_label (str, optional): Label of the x axis. Defaults to None.
        - y_label (str, optional): Label of the y axis. Defaults to None.
        - delimiter (str, optional): Delimiter of the CSV file. Defaults to ",".

    Returns:
        - None
    """
    sns.set_theme()

    # Control param possible errors
    if hue == "":
        hue = None
        palette = None

    if palette == "":
        palette = None

    if style == "" or style is None:
        style = None
        markers = None
        dashes = None

    # Read CSV file
    data = pd.read_csv(filepath, sep=delimiter)

    # Plot
    fig = plt.figure(figsize=(10, 10))

    sns.lineplot(
        data=data,
        x=x_column,
        y=y_column,
        hue=hue,
        style=style,
        markers=markers,
        dashes=dashes,
        palette=palette,
        errorbar=("ci", 95) if ci else None,  # 95% confidence interval
    )
    if legend:
        plt.legend(loc="upper left", fontsize=12, bbox_to_anchor=(1.05, 1))
    else:
        plt.legend().remove()

    plt.grid(grid)

    plt.title(title, fontsize=16, fontweight="bold") if title else None
    plt.xlabel(x_label) if x_label else None
    plt.ylabel(y_label) if y_label else None

    # Save plot
    file = f"{output_path}/lineplot"
    extensions = [".pdf", ".png", ".svg"]

    for ext in extensions:
        fig.savefig(f"{file}{ext}", bbox_inches="tight", dpi=300)


# ========= MAIN =========
if __name__ == "__main__":

    def __as_bool(value: str) -> bool:
        if value.lower() in ["true", "yes", "t", "y", "1"]:
            return True
        elif value.lower() in ["false", "no", "f", "n", "0"]:
            return False
        else:
            raise ValueError("Invalid boolean value")

    parser = ArgumentParser(description="Line chart plot")
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
        default=None,
        help="Palette of colors for the plot.",
        dest="palette",
        metavar="STRING",
    )
    parser.add_argument(
        "--style",
        type=str,
        required=False,
        default=None,
        help="Column name for styles of the lines.",
        dest="style",
        metavar="STRING",
    )
    parser.add_argument(
        "--markers",
        type=__as_bool,
        required=False,
        default=False,
        help="Show different markers. Must be with style param",
        dest="markers",
        metavar="BOOL",
    )
    parser.add_argument(
        "--dashes",
        type=__as_bool,
        required=False,
        default=False,
        help="Show different lines. Must be with style param",
        dest="dashes",
        metavar="BOOL",
    )
    parser.add_argument(
        "--grid",
        type=__as_bool,
        required=False,
        default=False,
        help="Show grid",
        dest="grid",
        metavar="BOOL",
    )
    parser.add_argument(
        "--ci",
        type=__as_bool,
        required=False,
        default=True,
        help="Show confidence interval of 95%%. None for quit interval.",
        dest="ci",
        metavar="BOOL",
    )
    parser.add_argument(
        "--legend",
        type=__as_bool,
        required=False,
        default="true",
        help="Show legend or not",
        dest="legend",
        metavar="BOOL",
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
        metavar="CHAR",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        required=False,
        default="/mnt/shared",
        help="Output path of the plot",
        dest="output",
        metavar="STRING",
    )

    args = parser.parse_args()

    line_chart(
        filepath=args.filepath,
        x_column=args.x_column,
        y_column=args.y_column,
        hue=args.hue,
        style=args.style,
        markers=args.markers,
        dashes=args.dashes,
        palette=args.palette,
        grid=args.grid,
        legend=args.legend,
        ci=args.ci,
        title=args.title,
        x_label=args.x_label,
        y_label=args.y_label,
        delimiter=args.delimiter,
        output_path=args.output,
    )
