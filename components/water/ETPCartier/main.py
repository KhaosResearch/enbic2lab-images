import pandas as pd
from argparse import ArgumentParser
import numpy as np

def main(
        filepath: str,
        delimiter: str,
        output: str,
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

    df["ETP Cartier (Hidro quebeq)"] = (0.02978*(df["TMAX"] - df["TMIN"]))*np.exp(0.019*(9/5*(df["TMAX"] + df["TMIN"])+64))

    

    df.to_csv(output, index=False, decimal=".", sep=delimiter)

if __name__ == "__main__":
    parser = ArgumentParser(description="ETP Cartier")
    parser.add_argument(
        "--filepath",
        type=str,
        help="Path to the CSV file with the necessary data to carry out the evapotranspiration calculation.",
        required=True,
    )
    
    parser.add_argument(
        "--delimiter",
        type=str,
        help="Delimiter of input file",
        default=";",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Path to the output CSV",
        default="/mnt/shared/"
    )

    args = parser.parse_args()

    main(
        args.filepath,
        args.delimiter,
        args.output + "output.csv",
    )

    