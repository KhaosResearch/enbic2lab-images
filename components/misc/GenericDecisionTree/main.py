import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree

from yellowbrick.classifier import (
    ConfusionMatrix,
    ClassPredictionError,
    ROCAUC,
    PrecisionRecallCurve,
)
import matplotlib.pyplot as plt

import skl2onnx

from argparse import ArgumentParser
from skl2onnx.common.data_types import FloatTensorType


def decision_tree(
    filepath_train: str,
    filepath_test: str,
    output: str,
    target_column: str,
    delimiter: str = ",",
) -> None:
    """Decision Tree

    This function trains a Decision Tree model and saves the results in the output path. It also saves the model in ONNX format and the metrics plots.

    Args:

        - filepath_train (str): File path to the CSV train dataset
        - filepath_test (str): File path to the CSV test dataset
        - output (str): Output path for the results
        - target_column (str): Target column
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

    model = DecisionTreeClassifier()
    model.fit(X=X_train, y=y_train)

    # ======= Plot tree =======
    fig = plt.figure(figsize=(25, 20))
    _ = tree.plot_tree(
        model,
        feature_names=X_train.columns,
        class_names=model.classes_,
        filled=True,
        rounded=True,
        fontsize=20
    )
    fig.savefig(f"{output}/tree.png", bbox_inches="tight", dpi=200)



    # ======= Save model =======
    onyx = skl2onnx.to_onnx(
        model=model,
        name=f"DecisionTree",
        X=X_train.values,
        initial_types=[("float_input", FloatTensorType([None, X_train.shape[1]]))],
        options={id(model): {"zipmap": False, "output_class_labels": True}},
    )

    with open(f"{output}/model.onnx", "wb") as f:
        f.write(onyx.SerializeToString())

    # ======= Metrics =======

    fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(nrows=2, ncols=2, figsize=(15, 15))

    # Confusion Matrix
    cm = ConfusionMatrix(model, classes=model.classes_, ax=ax1)
    cm.fit(X_train, y_train)
    cm.score(X_test, y_test)
    cm.finalize()

    # Class Prediction Error
    cpe = ClassPredictionError(model, classes=model.classes_, ax=ax2)
    cpe.fit(X_train, y_train)
    cpe.score(X_test, y_test)
    cpe.finalize()

    # Precision Recall Curve
    if len(model.classes_) == 2:
        prc = PrecisionRecallCurve(model, ax=ax3)
        prc.fit(X_train, y_train)
        prc.score(X_test, y_test)
    elif len(model.classes_) > 2:
        prc = PrecisionRecallCurve(
            model,
            per_class=True,
            iso_f1_curves=True,
            fill_area=False,
            micro=False,
            classes=model.classes_,
            ax=ax3,
        )
        prc.fit(X_train, y_train)
        prc.score(X_test, y_test)

    prc.finalize()

    # ROC AUC
    roc = ROCAUC(model, classes=model.classes_, micro=False, ax=ax4)
    roc.fit(X_train, y_train)
    roc.score(X_test, y_test)
    roc.finalize()

    fig.savefig(f"{output}/metrics.png", bbox_inches="tight", dpi=200)


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
        "--target-column",
        type=str,
        required=True,
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

    decision_tree(
        filepath_train=args.filepath_train,
        filepath_test=args.filepath_test,
        target_column=args.target_column,
        delimiter=args.delimiter,
        output=args.output,
    )
