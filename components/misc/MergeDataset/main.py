import argparse
import pandas as pd

def main(filepath1:str,filepath2:str, output: str, delimiter1: str = ";", delimiter2: str = ";") -> None:
    """
    Join CSV by Rows.
    Args:
        filepath1 (str): The path to the first CSV dataset file to be join.
        filepath2 (str): The path to the second CSV dataset file to be join.
        delimiter1 (str): Delimiter to use in the first output CSV file to separate values (e.g., ',' or ';').
        delimiter2 (str): Delimiter to use in the second output CSV file to separate values (e.g., ',' or ';').
        output (str): The path to save the join dataset as a new CSV file.

    """
    first_csv = pd.read_csv(filepath1, sep=delimiter1, index_col=False)
    second_csv = pd.read_csv(filepath2, sep=delimiter2, index_col=False)

    columns_first = set(first_csv.columns)

    columns_second = set(second_csv.columns)

    same_columns = False

    if columns_first == columns_second:
        same_columns = True
    else:
        raise ValueError("CSV files do not have the same columns.")

    if same_columns:
        result = pd.concat([first_csv, second_csv])
        final_csv = result.reset_index()
        final_csv = final_csv.drop("index", axis=1)
        final_csv.to_csv(output, sep=delimiter2, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Join CSV by column.")
    
    parser.add_argument(
        "--filepath1",
        type=str,
        required=False,
        help="Filepath of the input CSV file",
    )
    parser.add_argument(
        "--filepath2",
        type=str,
        required=False,
        help="Filepath of the input CSV file",
    )
    parser.add_argument(
        "--delimiter1",
        type=str,
        required=False,
        default=";",
        help="Delimiter of the CSV file",
    )
    parser.add_argument(
        "--delimiter2",
        type=str,
        required=False,
        help="Delimiter of the CSV file",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=False,
        help="Filepath of the output HTML file",
    )
    
    args = parser.parse_args()

    main(
        args.filepath1,
        args.filepath2,
        args.output,
        args.delimiter1,
        args.delimiter2
    )
