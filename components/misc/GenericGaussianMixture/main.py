import pandas as pd
from sklearn.mixture import GaussianMixture

import skl2onnx

from argparse import ArgumentParser


def gaussian_mixture(
    filepath_train: str,
    filepath_test: str,
    output: str,
    target_column: str = None,
    delimiter: str = ",",
) -> None:
    """Gaussion Mixture clustering

    This function trains a Gaussian Mixture clustering model and exports it to ONNX.

    Args:
        - filepath_train (str): File path to the CSV train dataset
        - filepath_test (str): File path to the CSV test dataset
        - output (str): Output path for the results
        - target_column (str): Target column of the dataset
        - delimiter (str): Delimiter of the CSV dataset
    
    Returns:
        None
    """
    df_train = pd.read_csv(filepath_train, delimiter=delimiter, decimal=".")
    df_test = pd.read_csv(filepath_test, delimiter=delimiter, decimal=".")

    if target_column is not None:
        X_train = df_train.drop(target_column, axis=1)
        y_train = df_train[target_column]
        X_test = df_test.drop(target_column, axis=1)
        y_test = df_test[target_column]
    else:
        X_train = df_train
        X_test = df_test

    # Create a Gaussian Mixture Model with 3 components
    model = GaussianMixture(covariance_type="full")

    # Fit the visualizer
    model.fit(X_train)

    # Export model to ONNX
    onyx = skl2onnx.to_onnx(
        model, X_train.values.astype("float32"), "gaussian_mixture.onnx"
    )

    with open(f"{output}/model.onnx", "wb") as f:
        f.write(onyx.SerializeToString())


if __name__ == "__main__":
    parser = ArgumentParser(description="Clustering with Gaussian Mixture")
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
        "--target-column",
        type=str,
        required=False,
        default=None,
        help="Target column of the dataset",
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

    gaussian_mixture(
        filepath_train=args.filepath_train,
        filepath_test=args.filepath_test,
        target_column=args.target_column,
        output=args.output,
        delimiter=args.delimiter,
    )
