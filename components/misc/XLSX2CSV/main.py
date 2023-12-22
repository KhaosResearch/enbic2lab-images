import pandas as pd
from argparse import ArgumentParser


# ============== METHODS ==============
def xlsx2csv(filepath: str, header: bool, output: str, delimiter: str = ";"):
    """Convert an Excel (XLSX) file to a CSV file.

    This function reads data from an Excel (XLSX) file and converts it to a CSV file format. You can specify whether the input file contains a header row and the delimiter to use in the CSV file.

    Args:
        filepath (str): The path to the Excel (XLSX) file to be converted to CSV.
        delimiter (str): Delimiter to use in the CSV file to separate values (e.g., ',' or ';').
        header (bool): Indicates whether the input file contains a header row with column names.
        output (str): The path to save the output CSV file.

    Example:
        To convert an Excel file 'data.xlsx' to a CSV file 'output.csv' with a semicolon (';') as the delimiter and a header row:

        >>> xlsx2csv(filepath="data.xlsx", delimiter=";", header=True, output="output.csv")

    Note:
        - The function uses the "openpyxl" engine to read Excel files.
        - The CSV file is saved with the specified delimiter, and the header row is included if specified.
    """

    # Read xlsx file
    if header:
        dataframe = pd.read_excel(filepath, engine="openpyxl")
    else:
        dataframe = pd.read_excel(filepath, engine="openpyxl", header=None)
    
    dataframe.replace("#VALUE!", None, inplace=True)
    
    # Export csv file
    dataframe.to_csv(output, sep=delimiter, index=None, decimal=".")


# ================= MAIN ===============
if __name__ == "__main__":
    parser = ArgumentParser(description="Convert XLSX to CSV")

    parser.add_argument(
        "--filepath",
        type=str,
        help="Filepath of the xlsx file.",
        required=True,
        metavar="STRING",
    )
    parser.add_argument(
        "--header",
        type=str,
        help="Wether the first row of the XLSX file is used as header or not",
        required=True,
        metavar="BOOL",
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
        "--delimiter",
        type=str,
        help="Delimiter of the CSV outfile",
        required=False,
        default=";",
        metavar="CHAR",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        help="Filepath of the CSV output file.",
        required=False,
        default="/mnt/shared",
        metavar="STRING",
        dest="output",
    )

    args = parser.parse_args()

    # Convert header argument to boolean
    if args.header in ["True", "true", "TRUE", "1", "yes", "Yes", "YES", "T", "t"]:
        args.header = True
    else:
        args.header = False

    xlsx2csv(
        filepath=args.filepath,
        delimiter=args.delimiter,
        header=args.header,
        output=args.output+"/output.csv",
    )
