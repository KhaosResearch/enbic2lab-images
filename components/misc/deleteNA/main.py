import pandas as pd
from argparse import ArgumentParser


def deleteNA(filepath: str, output: str, delimiter: str = ";", delete_option: str = "both"):
    """Delete missing values (NaN) from a dataset and save the cleaned dataset to a new CSV file.

    This function reads a CSV dataset, performs missing value removal based on the specified delete option, and saves the cleaned dataset to a new CSV file.

    Args:
        filepath (str): The path to the CSV dataset file to be cleaned.
        delimiter (str): Delimiter used in the CSV file to separate values (e.g., ',' or ';').
        output (str): The path to save the cleaned dataset as a new CSV file.
        delete_option (str): The delete option specifying which missing values to remove. Options: "column" (remove columns with all NaN values), "row" (remove rows with any NaN values), "both" (remove both columns and rows with NaN values). Default is "both".

    Raises:
        ValueError: If an invalid delete option is specified.

    Example:
        To clean a dataset 'data.csv' by removing rows and columns with missing values and save the cleaned dataset as 'cleaned_data.csv' with a semicolon (';') as the delimiter:

        >>> deleteNA(filepath="data.csv", delimiter=";", output="cleaned_data.csv", delete_option="both")

    Note:
        - The cleaned dataset is saved with the specified delimiter.
    """

    dataframe = pd.read_csv(filepath, sep=delimiter)

    columns = list(dataframe.columns)

    match delete_option:
        case "column":
            # For every column: if it is completely empty --> Remove it
            for column in columns:
                if dataframe[column].isnull().all():
                    dataframe = dataframe.drop([column], axis=1)
        case "row":
            # Remove all rows with any NaN values
            dataframe.dropna(axis=0, how="any", inplace=True)
        case "both":
            for column in columns:
                if dataframe[column].isnull().all():
                    dataframe = dataframe.drop([column], axis=1)
            dataframe.dropna(axis=0, how="any", inplace=True)
        case _:
            raise ValueError("Invalid delete option")

    dataframe.to_csv(output, sep=delimiter, index=False)


if __name__ == "__main__":
    parser = ArgumentParser(description="Delete columns, rows or both with NA values")
    parser.add_argument(
        "--filepath",
        type=str,
        help="File path of the csv file",
        required=True,
        metavar="STRING",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        help="Delimiter of the csv file",
        required=False,
        default=";",
        metavar="CHAR",
    )
    parser.add_argument(
        "--delete-option",
        dest="delete_option",
        type=str,
        help="String indicating whether to remove columns, rows or both with all NA values (row, column, both)",
        required=False,
        choices=["row", "column", "both"],
        default="both",
    ),
    parser.add_argument(
        "--output-path",
        type=str,
        help="File path of the output csv file",
        required=False,
        default="/mnt/shared",
        metavar="STRING",
        dest="output",
    )

    args = parser.parse_args()

    deleteNA(
        filepath=args.filepath,
        delimiter=args.delimiter,
        delete_option=args.delete_option,
        output=args.output+"/output.csv",
    )
