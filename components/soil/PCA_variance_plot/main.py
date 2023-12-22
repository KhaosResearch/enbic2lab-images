import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from argparse import ArgumentParser


def pca_variance_plot(filepath: str, delimiter: str, output: str):
    """Generate a scree plot from data in a CSV file.

    This function reads data from a CSV file, calculates the variance explained by different numbers of components, and creates a scree plot to visualize the variance explained. The plot is saved in PDF format.

    Args:
        filepath (str): The path to the CSV file containing the data for the scree plot.
        delimiter (str): Delimiter used in the CSV file to separate values (e.g., ',' or ';').
        output (str): The path to save the scree plot in PDF format.

    Raises:
        FileNotFoundError: If the output file could not be saved.

    Example:
        To create a scree plot from data in a CSV file 'data.csv' with ',' as the delimiter and save it as 'scree_plot.pdf':

        >>> pca_variance_plot(filepath="data.csv", delimiter=",", output="scree_plot.pdf")

    Note:
        - The function calculates the variance explained by different numbers of components and visualizes it as a scree plot.
        - The scree plot is saved in PDF format.
    """

    data = pd.read_csv(filepath, sep=delimiter, decimal=".", header=None)
    data.index += 1

    plt.style.use(
        "seaborn-v0_8-whitegrid"
    )  # Note: Custom style name may change with newer versions of matplotlib
    fig = plt.figure()
    ax = plt.axes()
    ax.set_xlabel("Number of Components")
    ax.set_ylabel("Variance")
    ax.plot(data, "bo", data, "k")
    plt.xticks(np.arange(0, len(data) + 1, 1.0))
    plt.title("Scree plot")

    try:
        fig.savefig(output, format="pdf")
    except:
        FileNotFoundError("The output file could not be saved.")


if __name__ == "__main__":
    parser = ArgumentParser(description="Plot the variance of the PCA")
    parser.add_argument(
        "--filepath",
        type=str,
        help="Path to the CSV file",
        required=True,
        metavar="STRING"
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        help="Delimiter of the CSV file",
        required=False,
        default=";",
        metavar="CHAR"
    )
    parser.add_argument(
        "--output-path",
        type=str,
        help="Path to the output file",
        required=False,
        default="/mnt/shared",
        metavar="STRING",
        dest="output"
    )

    args = parser.parse_args()

    pca_variance_plot(
        filepath=args.filepath,
        delimiter=args.delimiter,
        output=args.output+"/scree_plot.pdf",
    )
