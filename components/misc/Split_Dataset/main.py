from re import findall
import pandas as pd
from typing import List
from argparse import ArgumentParser


# ============ METHODS ============
def split_dataset(
    filepath: str,
    attribute_list: List[str],
    output: str,
    delimiter: str = ";"
) -> None:
    """Split a dataset by selecting specific attributes and save it to a new CSV file.

    This function reads a CSV dataset, selects specific attributes from the dataset, and saves the resulting dataset to a new CSV file. The attributes to keep are specified in the `attribute_list`.

    Args:
        filepath (str): The path to the CSV dataset file to be split.
        attribute_list (List[str]): A list of attribute names to be retained in the resulting dataset.
        delimiter (str): Delimiter to use in the output CSV file to separate values (e.g., ',' or ';').
        output (str): The path to save the split dataset as a new CSV file.

    Raises:
        ValueError: If not all attributes in the `attribute_list` are present in the dataset.

    Example:
        To split a dataset 'data.csv' by selecting attributes 'A', 'B', and 'C', and save the resulting dataset as 'output.csv' with a semicolon (';') as the delimiter:

        >>> split_dataset(filepath="data.csv", attribute_list=['A', 'B', 'C'], delimiter=';', output="output.csv")

    Note:
        - The resulting dataset is saved with the specified delimiter.
    """

    # Read data
    dataframe = pd.read_csv(filepath, sep=delimiter)

    # Chek if all attributes in attribute_list is in dataframe columns
    if all(x in dataframe for x in attribute_list):
        # Select columns to keep
        dataframe = dataframe[dataframe.columns.intersection(attribute_list)]
    else:
        raise ValueError(f"Not all attributes in list are in the dataframe. Possible values for this dataset: {', '.join(dataframe.columns)}")

    dataframe.to_csv(output, sep=delimiter, index=None)


# ============ MAIN ============
if __name__ == "__main__":
    parser = ArgumentParser(description="Split the dataset into the given columns")

    parser.add_argument(
        "--filepath",
        type=str,
        help="File path of the csv file",
        required=True,
        metavar="STRING"
    )
    parser.add_argument(
        "--attribute-list",
        dest="attribute_list",
        type=str,
        help="List of attributes that you want to keep. All must be in the dataframe. Insert the elements separated by commas (,)",
        required=True,
        metavar="STRING"
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        help="Delimiter of the input file and output file",
        required=False,
        default=";",
        metavar="CHAR"
    )
    parser.add_argument(
        "--output-path",
        type=str,
        help="Output path",
        required=False,
        default="/mnt/shared",
        metavar="STRING",
        dest="output"
    )

    args = parser.parse_args()

    # Convert attribute_list to list
    args.attribute_list = findall(r'\s*([^,]+)\s*', args.attribute_list)

    split_dataset(
        filepath=args.filepath,
        attribute_list=args.attribute_list,
        delimiter=args.delimiter,
        output=args.output+"/output.csv"
    )
