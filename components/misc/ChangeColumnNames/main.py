from pathlib import Path
import pandas as pd
from re import findall
import argparse

def rename_columns(df: pd.DataFrame, labels: list[str] = None) -> pd.DataFrame:
    if labels:
        new_names = [labels[i] if i < len(labels) else name for i, name in enumerate(df.columns)]
        return df.rename(columns=dict(zip(df.columns, new_names)))
    else:
        return df


def main(filepath:str, output:str, labels: list[str] = None,  delimiter:str=";"):
    print(labels)
    df = pd.read_csv(Path( filepath), sep=delimiter)
    df = rename_columns(df, labels)
    
    df.to_csv(output, sep=delimiter, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ETP Plot component")

    # Define command-line arguments
    parser.add_argument(
        "--filepath",
        type=str,
        required=True,
        help="Path to the input CSV file",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        default=";",
        required=True,
        help="Delimiter used in the input CSV File",
    )
    parser.add_argument(
        "--labels",
        type=str,
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
    args.labels = findall(r'\s*([^,]+)\s*', args.labels) if args.labels != None else None


    # Call the main function with provided arguments and specify the output file path
    main(args.filepath,  args.output, args.labels,  args.delimiter)
