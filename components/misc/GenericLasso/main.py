import pandas as pd
from sklearn.linear_model import Lasso

from yellowbrick.regressor import (
    PredictionError,
    ResidualsPlot,
    CooksDistance,
)
import matplotlib.pyplot as plt
import skl2onnx

from argparse import ArgumentParser
from skl2onnx.common.data_types import FloatTensorType


def lasso(
    filepath_train: str,
    filepath_test: str,
    target_column: str,
    output: str,
    alpha: float = 0.1,
    delimiter: str = ";",
) -> None:
    """Lasso Regression

    This function trains a Lasso Regression model and saves the results in the output path. It also saves the model in ONNX format and the metrics plots.

    Args:
        - filepath_train (str): File path to the CSV train dataset
        - filepath_test (str): File path to the CSV test dataset
        - output (str): Output path for the results
        - target_column (str): Target column
        - alpha (float): Alpha value
        - delimiter (str): Delimiter of the CSV dataset

    Returns:
            - None
    """
    train_df = pd.read_csv(filepath_train, delimiter=delimiter, decimal=".")
    test_df = pd.read_csv(filepath_test, delimiter=delimiter, decimal=".")

    try:
        X_train = train_df.drop(target_column, axis=1)
        y_train = train_df[target_column]
        X_test = test_df.drop(target_column, axis=1)
        y_test = test_df[target_column]
    except:
        raise ValueError(f"Target column ('{target_column}') not found in the dataset")

    model = Lasso(alpha=alpha)
    model.fit(X=X_train, y=y_train)

    # ======= Save model in ONNX format =======
    initial_type = [("float_input", FloatTensorType([None, X_train.shape[1]]))]
    onyx = skl2onnx.convert_sklearn(model, initial_types=initial_type)
    with open(f"{output}/model.onnx", "wb") as f:
        f.write(onyx.SerializeToString())

    # ======= Plot metrics =======

    fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(nrows=2, ncols=2, figsize=(15, 15))

    # Prediction error
    visualizer = PredictionError(model, is_fitted=True, ax=ax1)
    visualizer.score(X_test, y_test)
    visualizer.finalize()

    # Residuals plot
    visualizer = ResidualsPlot(model, is_fitted=True, ax=ax2)
    visualizer.score(X_test, y_test)
    visualizer.finalize()

    # Cook's distance
    visualizer = CooksDistance(ax=ax3)
    visualizer.fit(X_train, y_train)
    visualizer.finalize()

    ax4.axis("off")

    fig.savefig(f"{output}/metrics.png")


if __name__ == "__main__":
    parser = ArgumentParser()
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
        required=True,
        help="Target column",
        dest="target_column",
        metavar="STRING",
    )
    parser.add_argument(
        "--alpha",
        type=float,
        required=False,
        default=0.1,
        help="Alpha value",
        dest="alpha",
        metavar="FLOAT",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        default=";",
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

    lasso(
        filepath_train=args.filepath_train,
        filepath_test=args.filepath_test,
        target_column=args.target_column,
        alpha=args.alpha,
        delimiter=args.delimiter,
        output=args.output,
    )
