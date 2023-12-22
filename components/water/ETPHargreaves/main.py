import pandas as pd
from argparse import ArgumentParser

def etp_hargreaves(
        filepath: str,
        output: str,
        delimiter: str = ";",
):
    """Calculate potential evapotranspiration using the Hargreaves method.
    Args:
        filepath (str): The path to the data file containing data.
        output (str): The path to save the calculated potential evapotranspiration data.
        delimiter (str, optional): The delimiter used in the data file (default is ";").

    Returns:
        None
    """
    df = pd.read_table(filepath, delimiter=delimiter)

    df["ETP Hargreaves"] = 0.0135*(df["TMedia"] + 17.78)*df["Rs"]

    df.to_csv(output, index=False, decimal=".", sep=delimiter)

if __name__ == "__main__":
    parser = ArgumentParser(description="ETP Hargreaves")
    parser.add_argument(
        "--filepath",
        type=str,
        help="Path to the CSV file with the necessary data to carry out the evapotranspiration calculation.",
        required=True,
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Path to the output CSV",
        required=True,
        default="/mnt/shared/output.csv"
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        help="Delimiter of input file",
        required=False,
        default=";",
    )

    args = parser.parse_args()

    etp_hargreaves(
        args.filepath,
        args.output,
        args.delimiter
    )

    