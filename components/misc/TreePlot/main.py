import matplotlib.pyplot as plt
from matplotlib import colormaps
import pandas as pd
import squarify

import builtins
from re import findall
from argparse import ArgumentParser


# ========= METHODS =========
def treeplot(
    filepath: str,
    target: str,
    output_path: str,
    label: str = None,
    palette: str | list = "viridis",
    title: str = None,
    delimiter: str = ",",
):
    """Tree plot

    This function creates a tree plot from a csv file. The plot is saved as pdf, png and svg.

    Args:
        - filepath (str): Filepath of the csv file
        - target (str): Column name of the target
        - output_path (str): Output path for the plot
        - label (str, optional): Column name of the label. Defaults to None.
        - palette (str | list, optional): Color palette for plot. Defaults to "viridis".
        - title (str, optional): Title of the plot. Defaults to None.
        - delimiter (str, optional): Delimiter of the csv file. Defaults to ",".

    Returns:
        - None

    Raises:
        - ValueError: Invalid palette type. Please use a palette name or a list of colors.
    """
    # Read data
    data = pd.read_csv(filepath, sep=delimiter)

    # Default palette is viridis
    if palette == "" or palette is None:
        palette = "viridis"

    # Default title is None
    if title == "":
        title = None
   
    # Encode target if necessary
    if data[target].dtype == "object":
        etarget = data[target].value_counts().to_list()
        labels = data[target].value_counts().index.to_list()
        if label == "" or label is None:
            labels = [f"{labels[i]} [{etarget[i]}]" for i in range(len(labels))]
        else:
            labels = data[label].value_counts().index.to_list()
    else:
        etarget = data[target]
        labels = data[label]


    # Set color palette
    match type(palette):
        case builtins.str:
            cmap = plt.get_cmap(palette)
            colors = [cmap(i / len(etarget)) for i in range(1, len(etarget) + 1)]
        case builtins.list:
            colors = palette
        case _:
            raise ValueError(
                "Invalid palette type. Please use a palette name or a list of colors."
            )

    # Plot
    fig = plt.figure(figsize=(10, 10))
    squarify.plot(
        sizes=etarget,
        norm_x=100,
        norm_y=100,
        color=colors,
        label=labels,
        alpha=0.7,
        text_kwargs={"visible": False},
    )
    plt.legend(
        title=target.capitalize(),
        title_fontproperties={"weight": "bold"},
        loc="upper left",
        bbox_to_anchor=(1.0, 1.0),
        fontsize=10,
    )
    plt.title(title, fontsize=16, fontweight="bold", pad=20) if title != None else None

    # Save plot
    file = f"{output_path}/treeplot"
    extensions = [".pdf", ".png", ".svg"]

    for ext in extensions:
        fig.savefig(f"{file}{ext}", bbox_inches="tight", dpi=300)


# =========== MAIN ===========
if __name__ == "__main__":
    parser = ArgumentParser(description="Tree Plot")
    parser.add_argument(
        "--filepath",
        type=str,
        help="Filepath of the csv file",
        required=True,
        dest="filepath",
        metavar="STRING",
    )
    parser.add_argument(
        "--target-col",
        type=str,
        help="Column name of the x axis",
        required=True,
        dest="target",
        metavar="STRING",
    )
    parser.add_argument(
        "--label",
        type=str,
        help="Column name of the label",
        required=False,
        default=None,
        dest="label",
        metavar="STRING",
    )
    parser.add_argument(
        "--palette",
        type=str,
        help="Color palette for plot",
        required=False,
        default="viridis",
        dest="palette",
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
        help="Output path for the plot",
        required=False,
        default="/mnt/shared",
        dest="output",
        metavar="STRING",
    )

    args = parser.parse_args()

    # Check if palette is palette or list of colors
    palette_input = (
        findall(r"\s*([^,]+)\s*", args.palette) if args.palette != None else "viridis"
    )

    # Check if a valid palette name has been given
    if len(palette_input) == 1 and palette_input[0] in list(colormaps):
        print("Using palette: ", palette_input[0])
        args.palette = palette_input[0]
    # Check if the first element is a valid palette name
    elif len(palette_input) >= 1 and palette_input[0] in list(colormaps):
        print("Using palette: ", palette_input[0])
        args.palette = palette_input[0]
    # Check if a list of colors has been given
    elif len(palette_input) >= 1 and palette_input[0] not in list(colormaps):
        print("Using palette: ", palette_input)
        args.palette = palette_input
    # Else, use default palette
    else:
        print("Invalid palette name. Using default palette: viridis")
        args.palette = "viridis"

    treeplot(
        filepath=args.filepath,
        target=args.target,
        output_path=args.output,
        label=args.label,
        palette=args.palette,
        title=args.title,
        delimiter=args.delimiter,
    )
