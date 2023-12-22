import pandas as pd

from sklearn.model_selection import train_test_split

from argparse import ArgumentParser, ArgumentError


def train_test_splitter(
    filepath: str,
    output_path: str,
    target_column: str = None,
    predict_split: float = 0.1,
    train_split: float = 0.8,
    delimiter: str = ";",
):
    """Split a dataset into train, test and predict sets

    Args:
        - filepath (str): File path to the CSV dataset
        - output_path (str): Output path for the results
        - target_column (str) = None: Target column
        - predict_split (float) = 0.1: Predict split
        - train_split (float) = 0.8: Train split
        - delimiter (str) = ";": Delimiter
    Raises:
        - ValueError: Predict split must be between 0 and 1
        - ValueError: Train split must be between 0 and 1
    """
    if target_column == "":
        target_column = None
    if predict_split < 0 or predict_split >= 1:
        raise ValueError("Predict split must be between 0 and 1. Range: [0, 1)]")
    if train_split < 0 or train_split >= 1:
        raise ValueError("Train split must be between 0 and 1. Range: [0, 1)")

    df = pd.read_csv(filepath, sep=delimiter, decimal=".")

    predict_rows = int(len(df) * predict_split)
    
    df_predict = df.sample(n=predict_rows)
    df_left = df.drop(df_predict.index, axis=0).reset_index(drop=True)
    df_predict.reset_index(drop=True, inplace=True)

    if target_column != None:
        X = df_left.drop(target_column, axis=1)
        y = df_left[target_column]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, train_size=train_split, test_size=1 - train_split
        )
        df_train = pd.concat([X_train, y_train], axis=1)
        df_test = pd.concat([X_test, y_test], axis=1)
        df_predict = df_predict.drop(target_column, axis=1)

    else:
        df_train, df_test = train_test_split(
            df_left, train_size=train_split, test_size=1 - train_split
        )

    df_predict.to_csv(f"{output_path}/predict.csv", index=False, sep=delimiter)
    df_train.to_csv(f"{output_path}/train.csv", index=False, sep=delimiter)
    df_test.to_csv(f"{output_path}/test.csv", index=False, sep=delimiter)


if __name__ == "__main__":
    parser = ArgumentParser(description="Train Test Splitter")
    parser.add_argument(
        "--filepath",
        type=str,
        required=True,
        help="File path to the CSV dataset",
        dest="filepath",
        metavar="STRING",
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
        "--predict-split",
        type=float,
        required=False,
        default=0.1,
        help="Predict split",
        dest="predict_split",
        metavar="FLOAT",
    )
    parser.add_argument(
        "--train-split",
        type=float,
        required=False,
        default=0.8,
        help="Train split",
        dest="train_split",
        metavar="FLOAT",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        required=False,
        default=";",
        help="Delimiter",
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

    if args.predict_split < 0 or args.predict_split > 1:
        raise ArgumentError("Predict split must be between 0 and 1")
    if args.train_split < 0 or args.train_split > 1:
        raise ArgumentError("Train split must be between 0 and 1")

    train_test_splitter(
        filepath=args.filepath,
        predict_split=args.predict_split,
        target_column=args.target_column,
        train_split=args.train_split,
        delimiter=args.delimiter,
        output_path=args.output,
    )
