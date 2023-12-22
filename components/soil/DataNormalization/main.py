import pandas as pd
from sklearn.preprocessing import StandardScaler
from argparse import ArgumentParser


def data_normalization(
    filepath: str,
    delimiter: str,
    output: str,
    target_column: str = None,
):
    """Normalize and scale data from a CSV file.

    Reads data from a CSV file, normalizes it by centering and scaling, and saves the normalized data to a new CSV file.

    Args:
        - filepath (str): Name of the CSV file containing the data to be normalized.
        - delimiter (str): Delimiter used in the CSV file to separate values (e.g., ',' or ';').
        - output (str): Path to save the output CSV file.
        - target_column (str): Name of the target column. The default is None.

    Raises:
        - ValueError: If the provided CSV file is not in a valid format or cannot be read.

    Example:

        To normalize the data in a CSV file 'input_data.csv' using a semicolon (;) as the delimiter and save the normalized data to 'DataNormalized.csv':

        >>> data_normalization(filepath="input_data.csv", delimiter=";")

        This will generate a new CSV file named 'DataNormalized.csv' in the default output directory with the normalized data.
    """

    try:
        df = pd.read_csv(filepath, sep=delimiter).dropna()
    except:
        raise ValueError("The file input is not in the valid format")

    if target_column is not None:
        df_target_column = df[[target_column]]
        df = df.drop([target_column], axis=1)

    # Factors in the output
    factors = list(df)

    # Centering and scaling the data so that the means for each factor are 0 and the standard deviation are 1
    scaled_data = StandardScaler().fit_transform(df)

    # Create output dataframe
    scaled_df = pd.DataFrame(scaled_data, columns=factors)

    if target_column is not None:
        scaled_df = pd.concat([df_target_column, scaled_df], axis=1)

    # prepare output for the time series output
    scaled_df.to_csv(output, sep=delimiter, index=False)


if __name__ == "__main__":
    parser = ArgumentParser(description="Normalize and scale data from a CSV file")
    parser.add_argument(
        "--filepath",
        type=str,
        help="Path to the CSV file containing the data to be normalized",
        required=True,
        metavar="STRING",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        default=";",
        help="Delimiter used in the CSV file to separate values (e.g., ',' or ';')",
        required=False,
        metavar="CHAR",
    )
    parser.add_argument(
        "--target-column",
        dest="target_column",
        type=str,
        default=None,
        help="Name of the target column",
        required=False,
        metavar="STRING",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        default="/mnt/shared",
        help="Path to save the output CSV file",
        required=False,
        metavar="STRING",
        dest="output",
    )

    args = parser.parse_args()

    data_normalization(
        filepath=args.filepath,
        delimiter=args.delimiter,
        target_column=args.target_column,
        output=args.output+"/DataNormalized.csv",
    )
