import pandas as pd
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder

from argparse import ArgumentParser
from re import findall


def encode_categorical_data(
    filepath: str,
    output: str,
    delimiter: str = ",",
    exclude_columns: list = None,
):
    """Encode categorical data

    This function encodes categorical data from the given dataset and saves the results.

    Args:
        - filepath (str): File path to the CSV dataset
        - output (str): Output path for the results
        - delimiter (str) = ",": Delimiter of the CSV dataset
        - exclude_columns (list) = None: Columns to exclude from the encoding

    Returns:
        - None
    """
    df = pd.read_csv(filepath, delimiter=delimiter)

    df.dropna(
        inplace=True, thresh=len(df.index) / 2, axis=1
    )  # Drop columns with more than 50% NaN values
    df.dropna(inplace=True, how="any", axis=0)  # Drop rows with NaN values

    if exclude_columns is not None:
        columns_excluded = df[exclude_columns]
        df = df.drop(exclude_columns, axis=1)

    for column in df.select_dtypes(include=["object"]).columns:
        if df[column].nunique() <= 3:
            encoder = OneHotEncoder(sparse_output=False)
            onehot_data = encoder.fit_transform(df[column].values.reshape(-1, 1))
            onehot_columns = encoder.get_feature_names_out([column])
            df = pd.concat(
                [df, pd.DataFrame(onehot_data, columns=onehot_columns, index=df.index)],
                axis=1,
            )
            df.drop(column, axis=1, inplace=True)
        else:
            df[column] = OrdinalEncoder().fit_transform(
                df[column].values.reshape(-1, 1)
            )

    if exclude_columns is not None:
        columns_excluded.set_index(df.index, inplace=True)
        df = pd.concat([df, columns_excluded], axis=1)

    df.reset_index(drop=True, inplace=True)

    df.to_csv(f"{output}/output.csv", index=False, sep=delimiter, decimal=".")


if __name__ == "__main__":

    def __as_list(value: str) -> list[str] | None:
        return findall(r"\s*([^,]+)\s*", value) if value != None else None

    parser = ArgumentParser(description="Encode categorical data")

    parser.add_argument(
        "--filepath",
        type=str,
        required=True,
        help="File path to the CSV dataset",
        dest="filepath",
        metavar="STRING",
    )
    parser.add_argument(
        "--exclude-columns",
        type=__as_list,
        required=False,
        default=None,
        help="Columns to exclude from the encoding. Separate with commas",
        dest="exclude_columns",
        metavar="LIST",
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

    encode_categorical_data(
        filepath=args.filepath,
        exclude_columns=args.exclude_columns,
        delimiter=args.delimiter,
        output=args.output,
    )
