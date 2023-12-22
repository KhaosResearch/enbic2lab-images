from pathlib import Path
import argparse
import pandas as pd

def main(filepath1:str, filepath2:str,output:str, delimiter1:str, delimiter2:str):
    df = pd.read_csv(Path(filepath1), sep=delimiter1)
    df2 = pd.read_csv(Path(filepath2), sep=delimiter2)

    df_merge = pd.concat([df, df2], ignore_index=False, axis=1)
    df_merge.to_csv(output, sep=delimiter1, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ETP Plot component")

    # Define command-line arguments
    parser.add_argument(
        "--filepath1",
        type=str,
        default="/mnt/shared/species_alcornocales.csv",
        required=True,
        help="Path to the input CSV file",
    )
    parser.add_argument(
        "--filepath2",
        type=str,
        default="/mnt/shared/species_cabo_de_gata.csv",
        required=True,
        help="Path to the input CSV file",
    )
    parser.add_argument(
        "--delimiter1",
        type=str,
        default=";",
        required=True,
        help="Delimiter used in the input CSV File",
    )
    parser.add_argument(
        "--delimiter2",
        type=str,
        default=";",
        required=True,
        help="Delimiter used in the input CSV File",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Path to the output CSV file ",
    )
    args = parser.parse_args()
    # Call the main function with provided arguments and specify the output file path
    main(args.filepath1, args.filepath2, args.output, args.delimiter1, args.delimiter2)
