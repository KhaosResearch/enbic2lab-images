import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from argparse import ArgumentParser
from random import random


# ========= METHODS =========
def violinplot(
    filepath: str,
    output_path: str,
    x_column: str = None,
    y_column: str = None,
    hue: str = None,
    palette: str = "tab10",
    orient: str = "vertical",
    inner: str = "box",
    split: bool = False,
    title=None,
    delimiter: str = ",",
) -> None:
    """Violin Plot

    Args:
        - filepath (str): Filepath of the csv file
        - output_path (str): Output path
        - x_column (str, optional): Column name of the x axis. Defaults to None.
        - y_column (str, optional): Column name of the y axis. Defaults to None.
        - hue (str, optional): Column name for hue. Defaults to None.
        - palette (str, optional): Palette color. Defaults to "tab10".
        - orient (str, optional): Orientation of the plot. If 'horizontal' x_column must be numeric, if 'vertical' y_column must be numeric. Defaults to "vertical".
        - inner (str, optional): Type of plot inside the violin. Defaults to "box".
        - split (bool, optional): Use split mode with hue. Defaults to False.
        - delimiter (str, optional): Delimiter of the csv file. Defaults to ",".

    Raises:
        - ValueError: Invalid orientation. Use 'vertical' or 'horizontal'
        - ValueError: x_column must be a categorical column when using vertical orientation
        - ValueError: y_column must be a categorical column when using horizontal orientation

    Returns:
        - None
    """
    sns.set_theme()

    # Read csv file
    data = pd.read_csv(filepath, sep=delimiter)

    # Check if hue is valid
    if hue == "" or hue == None:
        hue = None
        split = False

    # Check if split is valid
    if split and len(data[hue].value_counts()) > 2:
        split = False

    # Check palette
    if palette == "" or palette == None:
        palette = None

    # Check inner type
    match inner.lower():
        case "box" | "quart" | "point" | "stick":
            pass
        case "none":
            inner = None
        case _:
            print("Invalid inner type. Using 'box' as default")
            inner = "box"

    x_column = None if x_column == "" else x_column
    y_column = None if y_column == "" else y_column

    # Check orientation
    match orient.lower():
        # Check if x_column is valid for vertical orientation
        case "vertical":
            if x_column != "" and x_column != None:
                # Check if x_column is categorical
                if data[x_column].dtype != "object":
                    # If x_column is not categorical, check if y_column is categorical. If so, swap x_column and y_column
                    if data[y_column].dtype == "object":
                        temp = x_column
                        x_column = y_column
                        y_column = temp
                    # If y_column is not categorical either, raise error
                    else:
                        raise ValueError(
                            "x_column must be a categorical column when using vertical orientation"
                        )
            # If x_column is not specified or is empty, set it to None
            else:
                x_column = None

        # Check if y_column is valid for horizontal orientation
        case "horizontal":
            # Check if y_column is specified and is not empty
            if y_column != "" and y_column != None:
                # Check if y_column is categorical
                if data[y_column].dtype != "object":
                    # If y_column is not categorical, check if x_column is categorical. If so, swap x_column and y_column
                    if data[x_column].dtype == "object":
                        temp = x_column
                        x_column = y_column
                        y_column = temp
                    # If x_column is not categorical either, raise error
                    else:
                        raise ValueError(
                            "y_column must be a categorical column when using horizontal orientation"
                        )
            # If y_column is not specified or is empty, set it to None
            else:
                y_column = None
        # If orientation is not valid, raise error
        case _:
            raise ValueError("Invalid orientation. Use 'vertical' or 'horizontal'")

    # Plot
    fig = plt.figure(figsize=(10, 10))
    sns.violinplot(
        data=data,
        x=x_column,
        y=y_column,
        hue=hue,
        orient=orient,
        inner=None,
        split=split,
        gap=0.1 if split else None,
        linewidth=0.75,
        alpha=0.85,
        palette=palette if hue is not None else None,
        color=plt.get_cmap(palette if palette != None else "tab10")(random())
        if hue == None
        else None,
    )
    plt.grid(True)
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1)) if hue is not None else None

    plt.title(title, fontsize=16, fontweight="bold") if title != None else None

    # Save plot
    file = f"{output_path}/violinplot"
    extensions = [".pdf", ".png", ".svg"]

    for ext in extensions:
        fig.savefig(f"{file}{ext}", bbox_inches="tight", dpi=300)


# =========== MAIN ===========
if __name__ == "__main__":

    def __as_bool(value):
        if value.lower() in ("yes", "true", "t", "y", "1"):
            return True
        elif value.lower() in ("no", "false", "f", "n", "0"):
            return False
        else:
            raise ValueError("Invalid value for boolean argument")

    parser = ArgumentParser(description="Violin Plot")

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
        required=False,
        default=None,
        help="Column name of the x axis",
        dest="x_column",
        metavar="STRING",
    )
    parser.add_argument(
        "--y-column",
        type=str,
        required=False,
        default=None,
        help="Column name of the y axis",
        dest="y_column",
        metavar="STRING",
    )
    parser.add_argument(
        "--hue",
        type=str,
        required=False,
        default=None,
        help="Column name for hue",
        dest="hue",
        metavar="STRING",
    )
    parser.add_argument(
        "--palette",
        type=str,
        required=False,
        default="tab10",
        help="Palette color",
        dest="palette",
        metavar="STRING",
    )
    parser.add_argument(
        "--orient",
        type=str.lower,
        required=False,
        default="vertical",
        help="Orientation of the plot. If 'horizontal' x_column must be numeric, if 'vertical' y_column must be numeric",
        choices=["vertical", "horizontal"],
        dest="orient",
        metavar="STRING",
    )
    parser.add_argument(
        "--inner",
        type=str,
        required=False,
        default="box",
        help="Type of plot inside the violin",
        choices=["box", "quart", "point", "stick", "none"],
        dest="inner",
        metavar="STRING",
    )
    parser.add_argument(
        "--split",
        type=__as_bool,
        required=False,
        default="false",
        help="Use split mode with hue",
        dest="split",
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
        help="Output path",
        dest="output",
        metavar="STRING",
    )

    args = parser.parse_args()

    violinplot(
        filepath=args.filepath,
        x_column=args.x_column,
        y_column=args.y_column,
        hue=args.hue,
        palette=args.palette,
        orient=args.orient,
        inner=args.inner,
        split=args.split,
        title=args.title,
        delimiter=args.delimiter,
        output_path=args.output,
    )
