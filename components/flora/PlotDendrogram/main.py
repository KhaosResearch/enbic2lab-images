import argparse

import pandas as pd
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage


def main(
    filepath: str,
    delimiter: str,
    metrdendrogram: str,
    methdendrogram: str,
    oriendendrogram: str,
    output: str,
) -> None:
    """
    Generates a hierarchical clustering dendrogram based on the given data.

    Args:
        filepath (str): The path to the CSV file.
        delimiter (str): The delimiter used in the CSV file.
        metrdendrogram (str): The metric used for calculating the distance between clusters.
        methdendrogram (str): The method used for clustering.
        oriendendrogram (str): The orientation of the dendrogram.
        output (str): The path to save the generated dendrogram image.
    """

    # Read CSV data
    data = pd.read_csv(filepath, sep=delimiter, decimal=".", index_col=0)
    df = data.iloc[:, :].values

    # Calculate figure size based on length of data
    if len(df) / 10 <= 10:
        x_ax = 15
        y_ax = 10
    else:
        x_ax = (len(df) / 10) + 5
        y_ax = 10

    # Calculate linkage and create figure
    Z = linkage(df, method=methdendrogram, metric=metrdendrogram)
    fig = plt.figure()

    # Set title and labels
    plt.title("Hierarchical Clustering Metric: " + metrdendrogram)
    plt.xlabel("Method: " + methdendrogram)
    plt.ylabel("Inventory")

    # Set figure size and orientation based on input
    if oriendendrogram == "top" or oriendendrogram == "bottom":
        fig.set_figheight(y_ax)
        fig.set_figwidth(x_ax)
        dendrogram(
            Z,
            leaf_rotation=90.0,
            orientation=oriendendrogram,
            labels=data.index.values,
            show_contracted=False,
        )
    else:
        fig.set_figheight(x_ax)
        fig.set_figwidth(y_ax)
        dendrogram(
            Z,
            labels=data.index.values,
            orientation=oriendendrogram,
            show_contracted=False,
        )

    # Save the generated figure
    plt.savefig(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot Dendrogram")

    parser.add_argument(
        "--filepath",
        type=str,
        required=True,
        help="Name of the csv file.",
    )

    parser.add_argument(
        "--delimiter",
        type=str,
        required=True,
        help="Delimiter of the csv file.",
    )

    parser.add_argument(
        "--metrdendrogram",
        type=str,
        required=True,
        choices=[
            "braycurtis",
            "canberra",
            "chebyshev",
            "cityblock",
            "correlation",
            "cosine",
            "dice",
            "euclidean",
            "hamming",
            "jaccard",
            "jensenshannon",
            "kulczynski1",
            "mahalanobis",
            "matching",
            "minkowski",
            "rogerstanimoto",
            "russellrao",
            "seuclidean",
            "sokalmichener",
            "sokalsneath",
            "sqeuclidean",
            "yule",
        ],
        help="Distance functions between numeric vectors. Choose from: 'braycurtis', 'canberra', 'chebyshev', 'cityblock', 'correlation', 'cosine', 'dice', 'euclidean', 'hamming', 'jaccard', 'jensenshannon', 'kulsinski', 'mahalanobis', 'matching', 'minkowski', 'rogerstanimoto', 'russellrao', 'seuclidean', 'sokalmichener', 'sokalsneath', 'sqeuclidean', 'yule'. Recommended options: 'euclidean' and 'sqeuclidean'.",
    )

    parser.add_argument(
        "--methdendrogram",
        type=str,
        required=True,
        choices=[
            "single",
            "complete",
            "average",
            "weighted",
            "median",
            "ward",
            "centroid",
        ],
        help="Methods for calculating the distance between the newly formed cluster. Choose from: 'single', 'complete', 'average', 'weighted', 'median', 'ward', 'centroide'. The 'median', 'ward', and 'centroid' methods are only available for the euclidean metric.",
    )

    parser.add_argument(
        "--oriendendrogram",
        type=str,
        required=True,
        choices=["top", "left", "bottom", "right"],
        help="The orientation of the dendrogram for visualization. Choose from: 'top', 'left', 'bottom', or 'right'.",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        help="[default value: /mnt/shared]",
        required=False,
        default="/mnt/shared",
        metavar="STRING",
        dest="output",
    )

    args = parser.parse_args()

    main(
        args.filepath,
        args.delimiter,
        args.metrdendrogram,
        args.methdendrogram,
        args.oriendendrogram,
        args.output+ "/output.pdf",
    )
