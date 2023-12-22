import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from argparse import ArgumentParser

# =========== METHODS ===========
def pairplot(
    filepath: str,
    output_path: str,
    kind: str = "scatter",
    diag_kind: str = "auto",
    hue: str = None,
    palette: str = None,
    title: str = None,
    delimiter: str = ",",
):
    """Pairplot
    This function generates a pairplot from a CSV file.

    Args:
        - filepath (str): File path of the CSV file
        - output_path (str): Path to save the plot
        - kind (str, optional): Kind of the plot. Defaults to "scatter".
        - diag_kind (str, optional): Diag kind of the plot. Defaults to "auto".
        - hue (str, optional): Column name for hue. Defaults to None.
        - palette (str, optional): Color palette of the plot. Defaults to None.
        - title (str, optional): Title of the plot. Defaults to None.
        - delimiter (str, optional): Delimiter of the CSV file. Defaults to ",".
    
    Returns:
        - None
    
    Raises:
        - ValueError: Invalid kind
        - ValueError: Invalid diag_kind
    """

    sns.set_theme()

    # Control parameters possible errors
    if hue == "":
        hue = None

    if palette == "":
        palette = None
    
    plot_kws = None
    diag_kws = None
    # Custom plot_kws and diag_kws for each kind
    match kind.lower():
        case "scatter":
            plot_kws = {"alpha": 0.7, "s": 80, "edgecolor": None}
        case "kde":
            plot_kws = {"alpha": 0.8}
        case "hist":
            plot_kws = {"linewidth": 0}
        case "reg":
            plot_kws = None
        case _:
            raise ValueError(f"Invalid kind: {kind}. Possible values are: scatter, kde, hist, reg")

    match diag_kind.lower():
        case "auto":
            if kind.lower() == "hist":
                diag_kws = {"linewidth": 0, "alpha": 0.7}
            else:
                diag_kws = {"alpha": 0.6}
        case "kde":
            diag_kws = {"alpha": 0.6}
        case "hist":
            diag_kws = {"linewidth": 0, "alpha": 0.7}
        case "none":
            diag_kind = None
            diag_kws = None
        case _:
            raise ValueError(f"Invalid diag_kind: {diag_kind}. Possible values are: auto, kde, hist, reg")
        
    # Read data
    data = pd.read_csv(filepath, sep=delimiter)

    # Generate plot
    pp = sns.pairplot(
        data,
        dropna=True,
        hue=hue,
        kind=kind,
        diag_kind=diag_kind,
        plot_kws=plot_kws,
        diag_kws=diag_kws,
        height=3,
        palette=palette
    )
    pp.figure.suptitle(title, y=1.05, fontsize=20, fontweight="bold") if title else None

    # Save plot
    file = f"{output_path}/pairplot"
    extensions = [".pdf", ".png", ".svg"]

    for ext in extensions:
        pp.savefig(f"{file}{ext}", bbox_inches="tight", dpi=300)


# =========== METHODS ===========
if __name__ == "__main__":
    parser = ArgumentParser(description="Generate pairplot")

    parser.add_argument(
        "--filepath",
        type=str,
        required=True,
        help="Filepath of the csv file",
        dest="filepath",
        metavar="STRING"
    )
    parser.add_argument(
        "--kind",
        type=str.lower,
        required=False,
        default="scatter",
        help="Kind of the plot.",
        choices=[
            "scatter",
            "kde",
            "hist",
            "reg"
        ],
        dest="kind",
        metavar="STRING"
    )
    parser.add_argument(
        "--diag-kind",
        type=str.lower,
        required=False,
        default="auto",
        help="Diag Kind of the plot. Possible values are: auto, kde, hist, reg",
        choices=[
            "auto",
            "kde",
            "hist",
            "none"
        ],
        dest="diag_kind",
        metavar="STRING"
    )
    parser.add_argument(
        "--hue",
        type=str,
        required=False,
        default=None,
        help="Hue of the plot",
        dest="hue",
        metavar="STRING"
    )
    parser.add_argument(
        "--palette",
        type=str,
        required=False,
        default=None,
        help="Palette of color for plot",
        dest="palette",
        metavar="STRING"
    )
    parser.add_argument(
        "--title",
        type=str,
        required=False,
        default=None,
        help="Title of the plot",
        dest="title",
        metavar="STRING"
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        required=False,
        default=",",
        help="Delimiter of the csv file",
        dest="delimiter",
        metavar="CHAR"
    )
    parser.add_argument(
        "--output-path",
        type=str,
        required=False,
        default="/mnt/shared",
        help="Output path of the plot",
        dest="output",
        metavar="STRING"
    )

    args = parser.parse_args()

    pairplot(
        filepath=args.filepath,
        hue=args.hue,
        kind=args.kind,
        diag_kind=args.diag_kind,
        palette=args.palette,
        title=args.title,
        delimiter=args.delimiter,
        output_path=args.output
    )