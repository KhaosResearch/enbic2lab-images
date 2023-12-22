import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from argparse import ArgumentParser


def pca_heatmap(
    filepath: str,
    output: str,
    delimiter: str = ";",
):
    """Generate a correlation heatmap from data in a CSV file.

    This function reads data from a CSV file, calculates the correlation matrix, and creates a heatmap to visualize the correlations between variables. The heatmap is saved in PDF format.

    Args:
        filepath (str): The path to the CSV file containing the data for the correlation heatmap.
        delimiter (str): Delimiter used in the CSV file to separate values (e.g., ',' or ';').
        output (str): The path to save the correlation heatmap in PDF format.

    Raises:
        FileNotFoundError: If the output file could not be created.

    Example:
        To create a correlation heatmap from data in a CSV file 'data.csv' with ';' as the delimiter and save it as 'correlation_heatmap.pdf':

        >>> pca_heatmap(filepath="data.csv", delimiter=";", output="correlation_heatmap.pdf")

    Note:
        - The function calculates the correlation matrix and visualizes it as a heatmap.
        - The heatmap is saved in PDF format.
    """

    data = pd.read_csv(str(filepath), sep=delimiter, decimal=".", index_col=0)
    labels = data.values.round(2)

    fig, ax = plt.subplots(figsize=(12, 11))
    title = "Correlation Matrix"
    plt.title(title, fontsize=18)
    ttl = ax.title
    ttl.set_position([0.5, 1.05])

    # Calculate font size based on the number of cells
    font_size = 150 / len(data)

    sns.heatmap(
        data,
        annot=labels,
        fmt="",
        cmap="coolwarm",
        linewidth=0.50,
        ax=ax,
        vmin=-1,
        vmax=1,
        annot_kws={"fontsize": font_size}  # Set the font size
    )
    plt.xticks(fontsize=7)
    plt.yticks(fontsize=7)

    try:
        fig.savefig(output, format="pdf")
    except:
        raise FileNotFoundError("The output file could not be created.")


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Plot the correlation matrix heatmap into a pdf file"
    )
    parser.add_argument(
        "--filepath",
        type=str,
        help="Path to the CSV file",
        required=True,
        metavar="STRING",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        help="Delimiter of the CSV file",
        required=False,
        default=";",
        metavar="CHAR",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        help="Path to save the correlation matrix heatmap in PDF format",
        required=False,
        default="/mnt/shared",
        metavar="STRING",
        dest="output",
    )

    args = parser.parse_args()

    pca_heatmap(
        filepath=args.filepath,
        delimiter=args.delimiter,
        output=args.output+"/heatmap_correlation_matrix.pdf",
    )
