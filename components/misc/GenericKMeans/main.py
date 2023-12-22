import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from yellowbrick.cluster import SilhouetteVisualizer, InterclusterDistance
import matplotlib.pyplot as plt

import skl2onnx

from argparse import ArgumentParser, ArgumentError


def __find_best_n_clusters(df_X: pd.DataFrame, max_iter: int = 10) -> int:
    """Find the best number of clusters

    This function finds the best number of clusters for the given dataset

    Args:
        - df_X (pd.DataFrame): Dataset
        - max_iter (int) = 10: Maximum number of iterations

    Returns:
        - int: Best number of clusters
    """
    s_score_prev = -1
    s_score = -1
    i = 1
    while s_score >= s_score_prev and i <= max_iter:
        i += 1
        s_score_prev = s_score
        model = KMeans(n_clusters=i, n_init=10, max_iter=300, tol=1e-04)
        model.fit(df_X.values)
        s_score = silhouette_score(df_X, model.labels_, metric="euclidean")

    return i - 1


def kmeans(
    filepath_train: str,
    filepath_test: str,
    output: str,
    target_column: str = None,
    n_clusters: int | str = "auto",
    delimiter: str = ",",
) -> None:
    """Main function for the clustering with KMeans

    This function fits a KMeans model to the given dataset, saves the model and plots the metrics.

    Args:
        - filepath (str): File path to the CSV dataset
        - output (str): Output path for the results
        - n_clusters (int|str) = "auto": Number of clusters
        - delimiter (str) = ",": Delimiter of the CSV dataset

    Returns:
        - None
    """
    if target_column == "":
        target_column = None
    # Load the datasets
    df_train = pd.read_csv(filepath_train, delimiter=delimiter, decimal=".")
    df_test = pd.read_csv(filepath_test, delimiter=delimiter, decimal=".")
    df = pd.concat([df_train, df_test], ignore_index=True)

    # Drop NA values
    df.dropna(inplace=True, thresh=len(df.index) / 2, axis=1) # Drop columns with more than 50% NaN values
    df.dropna(inplace=True, how="any", axis=0) # Drop rows with NaN values

    # Split the dataset
    if target_column is not None:
        df_X = df.drop(target_column, axis=1)
        df_y = df[target_column]
    else:
        df_X = df

    # Create the model
    if n_clusters == "auto":
        n_clusters = __find_best_n_clusters(df_X)
        model = KMeans(n_clusters=n_clusters, n_init=10, max_iter=300, tol=1e-04)
    elif isinstance(n_clusters, int):
        model = KMeans(n_clusters=n_clusters, n_init=10, max_iter=300, tol=1e-04)
    else:
        raise ValueError("n_clusters must be an integer or 'auto'")

    # Fit the model
    model.fit(df_X.values)

    # ======= Metrics =======
    fig, ax = plt.subplots(ncols=2, figsize=(12, 5))
    # Silhouette score
    # s_score = silhouette_score(df_X, model.labels_, metric="euclidean")
    # print("Silhouette score: ", s_score)

    sil_viz = SilhouetteVisualizer(model, colors="yellowbrick", ax=ax[0])
    sil_viz.fit(df_X.values)
    sil_viz.finalize()

    # Intercluster distance map

    inter_clus_viz = InterclusterDistance(model, ax=ax[1])
    inter_clus_viz.fit(df_X.values)
    inter_clus_viz.finalize()

    fig.savefig(f"{output}/metrics.png")

    # ======= Save model =======

    onyx = skl2onnx.to_onnx(model=model, name=f"KMeans", X=df_X.values)

    with open(f"{output}/model.onnx", "wb") as f:
        f.write(onyx.SerializeToString())


if __name__ == "__main__":
    parser = ArgumentParser(description="Clustering with KMeans")
    parser.add_argument(
        "--filepath-train",
        type=str,
        required=True,
        help="File path to the CSV train dataset",
        dest="filepath_train",
        metavar="STRING",
    )
    parser.add_argument(
        "--filepath-test",
        type=str,
        required=True,
        help="File path to the CSV test dataset",
        dest="filepath_test",
        metavar="STRING",
    )
    parser.add_argument(
        "--n-clusters",
        type=str,
        required=False,
        default="auto",
        help="Number of clusters",
        dest="n_clusters",
        metavar="INTEGER",
    )
    parser.add_argument(
        "--target-column",
        type=str,
        required=False,
        default=None,
        help="Target column",
        dest="target_column",
        metavar="STRING",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        required=False,
        default=",",
        help="Delimiter of the CSV dataset",
        dest="delimiter",
        metavar="CHAR",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        required=False,
        default="/mnt/shared",
        help="Output path for the results",
        dest="output",
        metavar="STRING",
    )

    args = parser.parse_args()

    if args.n_clusters == "auto":
        pass
    elif args.n_clusters.isdigit():
        args.n_clusters = int(args.n_clusters)
    else:
        raise ArgumentError("n_clusters must be an integer or 'auto'")

    kmeans(
        filepath_train=args.filepath_train,
        filepath_test=args.filepath_test,
        n_clusters=args.n_clusters,
        target_column=args.target_column,
        delimiter=args.delimiter,
        output=args.output,
    )
