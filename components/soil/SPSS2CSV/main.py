import pandas as pd
from argparse import ArgumentParser


def spss2csv(
    filepath: str,
    drop_index: bool,
    output: str,
) -> None:
    """
    Convert SPSS file to CSV format.

    This function reads data from an SPSS file, converts it to a CSV format, and saves it to a specified output file.

    Args:
        - filepath (str): The path to the SPSS file to be converted to CSV.
        - drop_index (bool): Indicates whether to drop the index column (if it exists) from the resulting CSV file.
        - output (str): The path to save the output CSV file.

    Raises:
        - ValueError: If the provided SPSS file is not in a valid format or cannot be read.

    Example:
        To convert an SPSS file 'data.sav' to a CSV file named 'output.csv' without dropping the index:

        >>> spss2csv(filepath="data.sav", drop_index=False, output="output.csv")

    Note:
        - The function will attempt to read the SPSS file and raise an error if the format is not valid.
        - The CSV file is saved with a semicolon (';') as the separator and without an index column unless specified otherwise.
    """

    # Create the dataframe
    try:
        df = pd.read_spss(filepath)
    except:
        raise ValueError("The format of the file is not valid")

    # Dropping the unname columns to obtain just the factors of analysis
    if "Unnamed: 0" in df.columns and drop_index:
        df = df.drop("Unnamed: 0", axis=1)

    # prepare the output
    df.to_csv(output, index=False, sep=";")


if __name__ == "__main__":
    parser = ArgumentParser(description="Convert SPSS file to CSV format")
    parser.add_argument(
        "--filepath",
        type=str,
        help="Path to the SPSS file to convert",
        required=True,
        metavar="STRING",
    )
    parser.add_argument(
        "--drop-index",
        type=str,
        help="Indicates whether to drop the index column (--drop-index) or not (--no-drop-index) from the resulting CSV file",
        required=True,
        metavar="BOOLEAN",
        dest="drop_index",
        choices=[
            "True",
            "False",
            "true",
            "false",
            "TRUE",
            "FALSE",
            "1",
            "0",
            "yes",
            "no",
            "Yes",
            "No",
            "YES",
            "NO",
            "T",
            "F",
            "t",
            "f"
        ],
    )
    parser.add_argument(
        "--output-path",
        type=str,
        help="Path to save the output CSV file",
        required=False,
        default="/mnt/shared",
        metavar="STRING",
        dest="output",
    )

    args = parser.parse_args()

    # Convert drop_index argument to boolean
    if args.drop_index in ["True", "true", "TRUE", "1", "yes", "Yes", "YES", "T", "t"]:
        args.drop_index = True
    else:
        args.drop_index = False

    spss2csv(
        filepath=args.filepath,
        drop_index=args.drop_index,
        output=args.output+"/Data.csv",
    )
