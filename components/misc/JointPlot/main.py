import pandas as pd
import seaborn as sns
from argparse import ArgumentParser

# =========== METHODS ===========
def jointplot(
    filepath: str,
    x_column: str,
    y_column: str,
    output_path: str,
    color: str = None,
    title = None,
    x_label = None,
    y_label = None,
    delimiter: str = ",",
) -> None:
    """Generate a joint plot from data in a CSV file and save the plot in multiple formats.

    Parameters:
        - filepath (str): The path to the input CSV file containing data for the joint plot.
        - x_column (str): The column to be used for the x-axis.
        - y_column (str): The column to be used for the y-axis.
        - output_path (str): The path to save the output plot files (PDF, PNG, SVG).
        - title (str, optional): The title of the plot. Default is None.
        - x_label (str, optional): The label for the x-axis. Default is None.
        - y_label (str, optional): The label for the y-axis. Default is None.
        - delimiter (str, optional): The delimiter used in the CSV file. Default is ",".
    
    Returns:
        None

    Usage:
        - This function reads data from a CSV file and generates a joint plot using seaborn.
        The resulting plot is saved in multiple formats (PDF, PNG, SVG).
    """
    # Read CSV file
    sns.set_theme()
    data = pd.read_csv(filepath, sep=delimiter)

    # Control possible errors
    if x_column == "" or y_column == "":
        raise ValueError("x_column and y_column cannot be empty")
    if data[x_column].dtype not in ["int64", "float64"]:
        raise ValueError(f"'{x_column}' must be a numeric column")
    if data[y_column].dtype not in ["int64", "float64"]:
        raise ValueError(f"'{y_column}' must be a numeric column")
    
    # Plot
    j = sns.jointplot(data=data, x=x_column, y=y_column, kind="reg", height=10, color=color)

    if title and title != "":
        j.figure.suptitle(title, fontsize=15, fontweight="bold", y=1.05)
    if x_label and x_label != "":
        j.ax_joint.set_xlabel(x_label, fontsize=12)
    if y_label and y_label != "":
        j.ax_joint.set_ylabel(y_label, fontsize=12)

    # Save plot
    file = f"{output_path}/jointplot"
    extensions = [".pdf", ".png", ".svg"]

    for ext in extensions:
        j.savefig(f"{file}{ext}", bbox_inches="tight", dpi=300)


# =========== MAIN ===========
if __name__ == "__main__":
    parser = ArgumentParser(description="Generic Joint Plot")
    parser.add_argument(
        "--filepath",
        type=str,
        help="Filepath of the CSV file",
        required=True,
        dest="filepath",
        metavar="STRING"
    )
    parser.add_argument(
        "--x-column",
        type=str,
        help="Name of the column for x axis",
        required=True,
        dest="x_column",
        metavar="STRING"
    )
    parser.add_argument(
        "--y-column",
        type=str,
        help="Name of the column for y axis",
        required=True,
        dest="y_column",
        metavar="STRING"
    )
    parser.add_argument(
        "--color",
        type=str,
        help="Color of the plot",
        required=False,
        default=None,
        dest="color",
        metavar="STRING"
    )
    parser.add_argument(
        "--title",
        type=str,
        help="Title of the plot",
        required=False,
        default=None,
        dest="title",
        metavar="STRING"
    )
    parser.add_argument(
        "--x-label",
        type=str,
        help="Label of the x-axis",
        required=False,
        default=None,
        dest="x_label",
        metavar="STRING"
    )
    parser.add_argument(
        "--y-label",
        type=str,
        help="Label of the y-axis",
        required=False,
        default=None,
        dest="y_label",
        metavar="STRING"
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        help="Delimiter of the CSV file",
        required=False,
        default=",",
        dest="delimiter",
        metavar="CHAR"
    )
    parser.add_argument(
        "--output-path",
        type=str,
        help="Path to save the output files",
        required=False,
        default="/mnt/shared",
        dest="output",
        metavar="STRING"
    )

    args = parser.parse_args()

    jointplot(
        filepath=args.filepath,
        x_column=args.x_column,
        y_column=args.y_column,
        color=args.color,
        title=args.title,
        x_label=args.x_label,
        y_label=args.y_label,
        delimiter=args.delimiter,
        output_path=args.output
    )