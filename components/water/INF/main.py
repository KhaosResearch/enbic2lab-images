import pandas as pd
import argparse


def main(
    filepath: str, output: str, delimiter: str = ";", p_zero: str = "0"
) -> None:
    """
    Calculate infiltration from an input CSV file..

    Args:
        filepath (str): Path to the input CSV file containing species data.
        delimiter (str): Delimiter used in the input CSV file to separate columns.
        p_zero (str): Parameter necessary to calculate the useful esc.
        output (str): Path to save the output CSV file with computed INF.
    """

    df = pd.read_table(filepath, delimiter=delimiter)

    df["ESC"] = ((df["LLU"] - float(p_zero)) ** 2) / (df["LLU"] + 4 * float(p_zero))

    df["ESC"] = df["ESC"].fillna(0)

    df["INF"] = df["LLU"] - df["ESC"]

    df["INF"].mask(df["INF"] < 0, float(0), inplace=True)

    df.to_csv(output, index=False, decimal=".", sep=delimiter)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="INF component")

    # Define command-line arguments
    parser.add_argument(
        "--filepath", type=str, required=True, help="Path to the input CSV File"
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        default=";",
        required=True,
        help="Delimiter used in the input CSV File",
    )
    parser.add_argument(
        "--p_zero",
        type=str,
        default="0",
        required=True,
        help="Parameter necessary to calculate the infiltration",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Path to the output CSV",
        required=True,
        default="/mnt/shared/InfiltrationData.csv"
    )

    args = parser.parse_args()

    # Call the main function with provided arguments and specify the output file path
    main(args.filepath, args.output, args.delimiter, args.p_zero)
